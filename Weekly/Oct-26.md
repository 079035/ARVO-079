# Findings of Codex Strategy

- Replace "line x" with "on the line start with xxx". Generally, get better results.
- Provide more specific vulnerability description, such as "off by one" rather than "heap overflow" - Case 3447
- Provide "less" code may achive better result in edit mode(More examples are needed to confirm) - Case 3447
- Insert Mode performs better than edit mode with the same instruction and code for uninit-variable vulnerability. Example is shown as following


# Insert Mode example:
Case 3447, Temperature == 0.05
```

class DngOpcodes::FixBadPixelsList final : public DngOpcodes::DngOpcode {
  std::vector<uint32> badPixels;

public:
  explicit FixBadPixelsList(const RawImage& ri, ByteStream* bs) {
public:
  explicit FixBadPixelsList(const RawImage& ri, ByteStream* bs) {

// The old code is "const iRectangle2D fullImage(0, 0, ri->getUncroppedDim().x,ri->getUncroppedDim().y);"
// The old code has off by one overflow vulnerability, insert a secure version of the old code. 
[Insert]

    bs->getU32(); // Skip phase - we don't care

    auto badPointCount = bs->getU32();
    auto badRectCount = bs->getU32();
    bs->check(2 * 4 * badPointCount + 4 * 4 * badRectCount);
    // Read points
    badPixels.reserve(badPixels.size() + badPointCount);
    for (auto i = 0U; i < badPointCount; ++i) {
      auto y = bs->getU32();
      auto x = bs->getU32();
      const iPoint2D badPoint(x, y);
      if (!fullImage.isPointInside(badPoint))
        ThrowRDE("Bad point not inside image.");
      badPixels.emplace_back(y << 16 | x);
}
```



