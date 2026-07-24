dev:
  rm -rf ./dist
  rm -rf ./build
  rm -rf .zig-out
  rm -rf .zig-cache
  zig build
  uv build --wheel
  uv pip install dist/*.whl

build-c:
  make -j 4
