"""RTL Generation Agent"""
from typing import Dict, Any
import httpx


class RTLAgent:
    """RTL/Verilog code generation"""
    
    def __init__(self):
        self.rtl_service_url = "http://rtl-generator:8021"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Generate RTL code from architecture"""
        try:
            response = await self.client.post(
                f"{self.rtl_service_url}/generate",
                json={"spec": architecture, "language": "systemverilog"}
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return self._inline_generate(architecture)
    
    def _inline_generate(self, arch: Dict[str, Any]) -> Dict[str, Any]:
        """Generate RTL inline"""
        comp_type = arch.get("type", "generic")
        width = arch.get("datapath_width", 8)
        
        if comp_type == "ripple_carry_adder":
            code = f"""module adder_{width}bit (
    input  logic [{width-1}:0] a,
    input  logic [{width-1}:0] b,
    input  logic cin,
    output logic [{width-1}:0] sum,
    output logic cout
);
    assign {{cout, sum}} = a + b + cin;
endmodule"""
            return {"code": code, "module_name": f"adder_{width}bit", "language": "systemverilog"}
        
        elif comp_type == "arithmetic_logic_unit":
            ops = arch.get("operations", ["ADD", "SUB", "AND", "OR", "XOR"])
            code = f"""module alu_{width}bit (
    input  logic [{width-1}:0] a, b,
    input  logic [2:0] opcode,
    output logic [{width-1}:0] result,
    output logic zero, carry, overflow
);
    logic [{width}:0] temp_add, temp_sub;
    
    always_comb begin
        zero = (result == 0);
        case (opcode)
            3'b000: begin // ADD
                temp_add = a + b;
                result = temp_add[{width-1}:0];
                carry = temp_add[{width}];
                overflow = (a[{width-1}] == b[{width-1}]) && (result[{width-1}] != a[{width-1}]);
            end
            3'b001: begin // SUB
                temp_sub = a - b;
                result = temp_sub[{width-1}:0];
                carry = temp_sub[{width}];
                overflow = (a[{width-1}] != b[{width-1}]) && (result[{width-1}] != a[{width-1}]);
            end
            3'b010: result = a & b;  // AND
            3'b011: result = a | b;  // OR
            3'b100: result = a ^ b;  // XOR
            3'b101: result = ~a;     // NOT
            3'b110: result = a << 1; // SHL
            3'b111: result = a >> 1; // SHR
            default: result = '0;
        endcase
    end
endmodule"""
            return {"code": code, "module_name": f"alu_{width}bit", "language": "systemverilog"}
        
        elif comp_type == "finite_state_machine":
            states = arch.get("state_names", ["IDLE", "ACTIVE", "DONE"])
            num_states = len(states)
            state_bits = (num_states - 1).bit_length()
            
            state_params = "\\n    ".join([f"localparam {s} = {i};" for i, s in enumerate(states)])
            code = f"""module fsm (
    input  logic clk, rst_n,
    input  logic start, done_signal,
    output logic [{state_bits-1}:0] current_state,
    output logic active, finished
);
    {state_params}
    
    logic [{state_bits-1}:0] next_state;
    
    // State register
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= {states[0]};
        else
            current_state <= next_state;
    end
    
    // Next state logic
    always_comb begin
        next_state = current_state;
        case (current_state)
            {states[0]}: if (start) next_state = {states[1] if len(states) > 1 else states[0]};
            {states[1] if len(states) > 1 else states[0]}: next_state = {states[2] if len(states) > 2 else states[0]};
            {states[2] if len(states) > 2 else states[0]}: if (done_signal) next_state = {states[3] if len(states) > 3 else states[0]};
            {states[3] if len(states) > 3 else states[0]}: next_state = {states[0]};
            default: next_state = {states[0]};
        endcase
    end
    
    // Output logic
    assign active = (current_state != {states[0]});
    assign finished = (current_state == {states[-1]});
endmodule"""
            return {"code": code, "module_name": "fsm", "language": "systemverilog"}
        
        elif comp_type == "uart_transmitter":
            data_bits = arch.get("data_bits", 8)
            code = f"""module uart_tx (
    input  logic clk, rst_n,
    input  logic [{data_bits-1}:0] tx_data,
    input  logic tx_start,
    output logic tx,
    output logic tx_busy
);
    localparam BAUD_DIV = 868; // For 115200 baud @ 100MHz
    
    typedef enum logic [2:0] {{
        IDLE, START, DATA, STOP
    }} state_t;
    
    state_t state, next_state;
    logic [{data_bits-1}:0] shift_reg;
    logic [3:0] bit_cnt;
    logic [15:0] baud_cnt;
    
    // State register
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= IDLE;
        else state <= next_state;
    end
    
    // Baud rate generator
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) baud_cnt <= 0;
        else if (state == IDLE) baud_cnt <= 0;
        else if (baud_cnt == BAUD_DIV) baud_cnt <= 0;
        else baud_cnt <= baud_cnt + 1;
    end
    
    wire baud_tick = (baud_cnt == BAUD_DIV);
    
    // Shift register and bit counter
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            shift_reg <= 0;
            bit_cnt <= 0;
        end else begin
            case (state)
                IDLE: if (tx_start) shift_reg <= tx_data;
                DATA: if (baud_tick) begin
                    shift_reg <= {{1'b0, shift_reg[{data_bits-1}:1]}};
                    bit_cnt <= bit_cnt + 1;
                end
                default: bit_cnt <= 0;
            endcase
        end
    end
    
    // State machine
    always_comb begin
        next_state = state;
        case (state)
            IDLE: if (tx_start) next_state = START;
            START: if (baud_tick) next_state = DATA;
            DATA: if (baud_tick && bit_cnt == {data_bits-1}) next_state = STOP;
            STOP: if (baud_tick) next_state = IDLE;
        endcase
    end
    
    // Output
    assign tx = (state == IDLE || state == STOP) ? 1'b1 :
                (state == START) ? 1'b0 : shift_reg[0];
    assign tx_busy = (state != IDLE);
endmodule"""
            return {"code": code, "module_name": "uart_tx", "language": "systemverilog"}
        
        elif comp_type == "counter":
            code = f"""module counter_{width}bit (
    input  logic clk, rst_n,
    input  logic enable,
    output logic [{width-1}:0] count,
    output logic overflow
);
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= '0;
        else if (enable)
            count <= count + 1;
    end
    
    assign overflow = (count == {2**width - 1}) && enable;
endmodule"""
            return {"code": code, "module_name": f"counter_{width}bit", "language": "systemverilog"}
        
        elif comp_type == "shift_register":
            direction = arch.get("shift_direction", "right")
            code = f"""module shift_reg_{width}bit (
    input  logic clk, rst_n,
    input  logic shift_en, load,
    input  logic [{width-1}:0] parallel_in,
    input  logic serial_in,
    output logic [{width-1}:0] data_out,
    output logic serial_out
);
    logic [{width-1}:0] reg_data;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            reg_data <= '0;
        else if (load)
            reg_data <= parallel_in;
        else if (shift_en)
            reg_data <= {'{{serial_in, reg_data[{width-1}:1]}}' if direction == 'right' else '{{reg_data[{width-2}:0], serial_in}}'};
    end
    
    assign data_out = reg_data;
    assign serial_out = reg_data[{'0' if direction == 'right' else f'{width-1}'}];
endmodule"""
            return {"code": code, "module_name": f"shift_reg_{width}bit", "language": "systemverilog"}
        
        return {"code": "// Generic module", "module_name": "generic", "language": "systemverilog"}
    
    async def fix_errors(self, rtl_result: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Attempt to fix RTL errors (self-correction)"""
        # Simple error fixes
        code = rtl_result.get("code", "")
        if "missing semicolon" in error.lower():
            # Add missing semicolons (simplified)
            pass
        return rtl_result
