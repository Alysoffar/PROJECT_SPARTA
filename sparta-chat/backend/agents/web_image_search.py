import os
import httpx
from typing import Optional


KEYWORD_IMAGE_MAP = {
    # Deterministic, topic-relevant images (schematics, breadboards, logic)
    "adder": [
        # Full adder truth table/logic gate diagram (Wikimedia)
        "https://upload.wikimedia.org/wikipedia/commons/6/6c/Full-adder.svg",
        # Breadboard-style electronics image (Pexels)
        "https://images.pexels.com/photos/257736/pexels-photo-257736.jpeg?w=1600",
    ],
    "alu": [
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/ALU_block_diagram.svg",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
    ],
    "counter": [
        "https://upload.wikimedia.org/wikipedia/commons/f/fb/4-bit_binary_counter.svg",
        "https://images.pexels.com/photos/159201/circuit-board-print-plate-via-macro-159201.jpeg?w=1600",
    ],
    "mux": [
        "https://upload.wikimedia.org/wikipedia/commons/4/47/Multiplexer_diagram.svg",
        "https://images.unsplash.com/photo-1553406830-ef2513450d76?w=1600&q=80",
    ],
    "demux": [
        "https://upload.wikimedia.org/wikipedia/commons/3/3b/Demultiplexer_diagram.svg",
        "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=1600&q=80",
    ],
    "flip-flop": [
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/JK_FF.svg",
        "https://images.pexels.com/photos/442152/pexels-photo-442152.jpeg?w=1600",
    ],
    "register": [
        "https://upload.wikimedia.org/wikipedia/commons/3/38/Shift_register.svg",
        "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=1600&q=80",
    ],
    "uart": [
        "https://upload.wikimedia.org/wikipedia/commons/3/34/UART_block_diagram.svg",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
    ],
}


async def fetch_first_image(query: str, output_dir: str = "static/generated") -> Optional[str]:
    """
    Deterministically fetch an image relevant to the hardware keyword.
    - If a known keyword is present, use its curated URLs (schematics/breadboards).
    - Otherwise return None (caller decides fallback behavior).
    """
    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    q = query.lower()
    matched_key = None
    for key in KEYWORD_IMAGE_MAP.keys():
        if key in q:
            matched_key = key
            break

    # Special handling: detect "adder" variants like "4-bit adder"
    if not matched_key and "adder" in q:
        matched_key = "adder"

    if not matched_key:
        print(f"[WebImageSearch] No keyword match in query: {query}")
        return None

    urls = KEYWORD_IMAGE_MAP[matched_key]
    print(f"[WebImageSearch] Keyword '{matched_key}' matched. Trying {len(urls)} URLs...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        for url in urls:
            try:
                print(f"[WebImageSearch] Downloading: {url}")
                resp = await client.get(url, follow_redirects=True)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    # Decide extension
                    ext = ".jpg"
                    if url.endswith(".svg"):
                        ext = ".svg"
                    elif url.endswith(".png"):
                        ext = ".png"

                    filename = f"web_{matched_key}_{abs(hash(url))}{ext}"
                    path = os.path.join(output_dir, filename)
                    with open(path, "wb") as f:
                        f.write(resp.content)
                    print(f"[WebImageSearch] ✅ Saved: {path}")
                    return path
                else:
                    print(f"[WebImageSearch] Skipped (status {resp.status_code} / small payload)")
            except Exception as e:
                print(f"[WebImageSearch] Error fetching {url}: {e}")

    print(f"[WebImageSearch] ❌ All curated URLs failed for '{matched_key}'")
    return None
