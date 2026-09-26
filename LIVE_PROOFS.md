# Live StudioNet proofs

Corrected StudioNet contract: [0xe3afE422EFe1aB4971E6045c5852A7Ff7bFD7c50](https://explorer-studio.genlayer.com/address/0xe3afE422EFe1aB4971E6045c5852A7Ff7bFD7c50), chain ID 61999. `genlayer code` returned source equal to [`contracts/DynamicKnowledgeMarketplace.py`](contracts/DynamicKnowledgeMarketplace.py) after newline normalization (13,786 characters). All proof transactions below reached `FINALIZED`; stored states were read afterward. Direct tests do not exercise validator consensus.

| Step | Finalized transaction | Stored result |
| --- | --- | --- |
| Corrected deployment | [0xf66f52b5…](https://explorer-studio.genlayer.com/tx/0xf66f52b5327d0f4af8d125219a75683d4b7b3061a0e27076c14e888b3504652a) | Contract execution succeeded |
| Create bounded exchange space | [0xc3d43a9b…](https://explorer-studio.genlayer.com/tx/0xc3d43a9bb37647e7d8839bcb16bccc6755ece46946a7eb56c72b4c7c7c593f52) | `water-sample-demo` |
| Register field source commitment | [0xe91a4f2e…](https://explorer-studio.genlayer.com/tx/0xe91a4f2e96d356ce6ddf5949a1c11831d470bba471b0c7bc329b2c381115ed52) | SHA-256 `5f6fbbb1…` |
| Register lab source commitment | [0x393c4e27…](https://explorer-studio.genlayer.com/tx/0x393c4e27b698ed62f5e373420821dc4492478b8657442f57ce1bd9a9299f25cb) | SHA-256 `58831612…` |
| Propose faithful merge | [0x9de2e969…](https://explorer-studio.genlayer.com/tx/0x9de2e9698377ec6f2ccbf7afea8d3cdcdc5c71f13853c50b16e66d0092b20b9d) | Immutable input/output binding |
| Apply faithful merge | [0x149198a1…](https://explorer-studio.genlayer.com/tx/0x149198a16224d1ff34d745202f8fbc4beca8739fc996f8220a00ff6af9b8e520) | `PUBLISHED`; all three fetched bodies HTTP 200 and hash-matched; vector `PASS/PASS/PASS/PASS`; root `adf8cf8644259db5985fdf294c82b01102526b0cab683e39149dbae2286cda65` |
| Propose meaning-reversing merge | [0xea1adfe0…](https://explorer-studio.genlayer.com/tx/0xea1adfe03fbba0a7509867ac0c6da7c431e848e8c6f95153286f6ab2da604cca) | Exact adversarial output commitment |
| Apply meaning-reversing merge | [0xa300e3d5…](https://explorer-studio.genlayer.com/tx/0xa300e3d5f3db999912c1c2d2385e5a53f7bf63ef8b13296352ea847e8340eca3) | `REJECTED`; all hashes matched, vector `FAIL/FAIL/FAIL/FAIL`; no asset; root `31df7e6c27be39dd580d87f34ee2a61db6d29e3d388a970d4bd867aa241d8193` |
| Propose wrong output commitment | [0x33d29db3…](https://explorer-studio.genlayer.com/tx/0x33d29db3a66c13bbf12956670321bed455316af001abb3d688d9196dbca95d2d) | Expected SHA-256 is deliberately incorrect |
| Apply wrong commitment | [0x1fe800ef…](https://explorer-studio.genlayer.com/tx/0x1fe800ef896e06e9af703f85f7e46b8aa0a6795ee0e00cdf5d41aaa91d844f66) | `INCONCLUSIVE`; hash matches `[true,true,false]`, vector `UNKNOWN/UNKNOWN/UNKNOWN/UNKNOWN`; no asset; root `e48a183be9163c44625dd3336d6e52844d2f6d81b08a48b88a67e38682dcd63b` |

Post-transaction `get_space("water-sample-demo")` returned `sources=2`, `transformations=3`, `derived=1`. `get_record` returns the complete decision-bearing report for each transform; `get_transform` returns its terminal state and root. The fixture texts are illustrative, pinned to [commit `f81d2a9`](https://github.com/Starling-spell/dynamic-knowledge-marketplace/tree/f81d2a9e84c137ac97b4c3adc25f1ea24f96f5a0/examples). The protocol proves faithful transformation of those fetched bytes, not the truth of water-sampling instructions.

An earlier contract at `0x1569E2D6cB33919b0770fD382b21f4ee82B53AE9` was superseded after the Windows CLI mishandled an empty optional argument. Its failed proposal calls are not presented as usage proofs. The corrected deployed source makes that argument optional and was independently linted and retested before deployment.
