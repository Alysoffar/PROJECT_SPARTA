#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ajvPackagePath = path.join(__dirname, '../node_modules/ajv/package.json');

if (fs.existsSync(ajvPackagePath)) {
  const ajvPackage = JSON.parse(fs.readFileSync(ajvPackagePath, 'utf8'));
  
  if (!ajvPackage.exports) {
    ajvPackage.exports = {
      ".": "./dist/index.js",
      "./dist/compile/codegen": "./dist/compile/codegen/index.js",
      "./dist/compile/context": "./dist/compile/index.js",
      "./dist/*": "./dist/*.js"
    };
    
    fs.writeFileSync(ajvPackagePath, JSON.stringify(ajvPackage, null, 2));
    console.log('✓ Patched ajv package.json with exports field');
  }
} else {
  console.log('⚠ ajv not found, skipping patch');
}
