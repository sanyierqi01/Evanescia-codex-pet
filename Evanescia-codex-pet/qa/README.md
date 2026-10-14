# 检查记录

此目录中的 JSON 是发布图集原始验证结果的脱敏副本，仅将机器绝对路径替换为相对来源标签，检查结论与警告保留。不会附带账号、云端宠物 ID 或 Library 上传记录。

- `pet-quality.json`：综合质量结果、图集摘要、跳跃离地 28 像素及落地偏差 0。
- `blind-validation.json`：多位独立方向盲审结果的合并校验。
- `direction-semantics.json`、`look-continuity.json`：方向与连续性检查记录。
- `pets-mcp-validation.json`：最终图集在 Pets 服务中的结构预检结果。

质量结果为通过，同时保留四个中间视角的人工复核警告和发丝/服饰轮廓空隙提示。请在 `assets/previews/direction-sheet.png` 中直接查看实际视角。

这些记录产生于素材制作时。仓库自带 `scripts/validate_atlas.py` 仅用于公开版本的结构与摘要复核，不重现 AI 制作过程或原服务全部检查。
