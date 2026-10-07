# Launched IMD community coins and project-linked swarm jobs

Snapshot taken 2026-10-07 (UTC) from the public IMD control-plane API documented at <https://www.imd.fun/docs/>, which is the API the explorer at <https://explorer.imd.fun> reads.

## Method and sources (facts)

- Coins: `GET https://api.imd.fun/publications?type=tokens&pageSize=100&page=1..3`. The docs describe this as the list of contracts whose launch minted a token. It returned 224 items, all with status `live`. Pages shifted while they were being fetched, so duplicate contract IDs were removed.
- Jobs: `GET https://api.imd.fun/jobs?limit=500`, paged backwards with `before=`. That gave 9327 jobs. 147 of them carry a non-null `project` field, spread across 53 distinct project IDs.
- Links: every link below was copied from a field in the record (`sourceRepoUrl`, `sites[].url`, `delivery.repoUrl`, `delivery.pullRequestUrl`) or taken from URLs written in a job's objective text. I added no outside links. **I did not guess any X/Twitter profiles.** Only one X profile appears in the records: <https://x.com/IaMaDamIMD>, written into the objective text of the `$ADAM` jobs as "official X". That label is the requester's own claim and was not verified.
- To check any coin, open `https://api.imd.fun/launches/<launch id>`. To check any job, open `https://api.imd.fun/jobs/<job id>`.

## Interpretation (inferences, labelled)

- *Inference:* "Community coins" is taken to mean every live launch that minted a token. This covers the kinds `custom_token`, `univ4_hook` and `evm_project`. The API has no separate "community coin" endpoint (`/coins` and `/community-coins` return 404). Parked or abandoned launches are left out because they are not launched.
- *Inference:* "Jobs that name a project" is taken to mean jobs whose record has a structured `project` reference `{id, version, of}`. A job whose free-text objective mentions a name, with no `project` field, is not counted.

## Uncertainty and unanswered questions

- The API returns job objectives cut off at about 160 characters (ending in `…`). Any link that appears only in the full objective text is not captured here.
- Project records have no human-readable project name. The API gives a UUID only, so the name shown is the job objective, which usually names the project.
- I found no public endpoint that lists projects directly. The `/workflows` endpoint was not explored.
- This is a point-in-time snapshot. New launches and jobs appear every few minutes.
- Unanswered: official X/social accounts for every coin except `$ADAM` (see above). No coin launch record has a social field.
- Whether these records are accurate on-chain was not checked independently. Addresses and tx hashes are reported exactly as the API gives them.

## A. Launched coins (224)

| # | Token (symbol) | Kind | Token address | Launch id | Links in record |
|---|---|---|---|---|---|
| 947 | IMDIVIDENDS (DIVIDENDS) | custom_token | `0xf08b07b740df2aaa939eea6b7bf66b44908341b9` | `150d4c2a-9d94-4ac9-92c1-c860d5486078` | <https://github.com/identity-md-launches/launch-947-imdividends> |
| 946 | IMDOLAR (DOLAR) | custom_token | `0x18150e743cf534346bc20df5e6f6ed06ea35a71c` | `379df038-912b-4616-97e4-70a15f400312` | <https://github.com/identity-md-launches/launch-946-imdolar> |
| 945 | 1 Million Dolar (1MD) | custom_token | `0x047ceafe0e715b7af38b65dd7185c60d9420594c` | `32d6fa78-991a-4402-a9ed-d80dc24e90dc` | <https://github.com/identity-md-launches/launch-945-1-million-dolar> |
| 944 | EmberEVO (EMBEO) | evm_project | `0x2b82cdeb8477415d541799abb0cc48044c8ea5f3` | `b81f8d6e-ebc0-4eb0-9307-d22cf765bea4` | <https://github.com/identity-md-launches/launch-944-emberevo-token-symbol-embeo> |
| 922 | Panic Monkeys (PANIC) | univ4_hook | `0xe52ab551160a74afed336c1fbf0f5d39b6fd4bba` | `78f747c8-2875-4984-a053-c0777cff1904` | <https://github.com/identity-md-launches/launch-922-start-existing-code-reuse> |
| 909 | imdDRONE (DRONE) | univ4_hook | `0xf0655276faefe9cd76d91f8f9ee50172f37d45c4` | `7279e66c-8c3d-4bc4-94fa-0ce43867d631` | <https://github.com/identity-md-launches/launch-909-launch-imddrone-token-name> |
| 904 | EmberEvo (EMVO) | evm_project | `0x7a427b94547232356cf212fd1c668e8eb4069a46` | `aea3dca5-1186-4f88-8f0a-a8c1246933ba` | <https://github.com/identity-md-launches/launch-904-emberevo-token-symbol-emvo> |
| 903 | Cets (CETS) | custom_token | `0x40ee61fdabe76d966a29ea406233ed80eb318410` | `8bcc66cf-db1d-4de2-95e2-bcd025975d66` | <https://github.com/identity-md-launches/launch-903-cets> |
| 892 | HFROG (HFROG) | univ4_hook | `0xbe349c4e13fc788db48e11152ae83c3b902b0b98` | `d9de490d-6104-4c49-8ce3-8194a1cba46c` | <https://github.com/identity-md-launches/launch-892-hash-frog-browser-mined-pow> |
| 884 | Quantum Observatory (QOBS) | evm_project | `0xad455ee2800b314588b5178df0dcbbc5dad7e1c7` | `1626c779-cfae-4288-b1eb-990d16d219f3` | <https://github.com/identity-md-launches/launch-884-workflow-contract-stage-context> |
| 882 | imdUSD (IMDUSD) | custom_token | `0x52b4f1a53d5919d08c6c60b31bd97dd901c88879` | `b0e218c6-9253-4e07-b6c7-906aca155626` | <https://github.com/identity-md-launches/launch-882-imdusd> |
| 881 | HS XWesXkAAMSB0 (HX) | evm_project | `0xe7b5b05cfebb11d08033020acdeb89fe672b0855` | `980fdec8-cbe6-44fd-af21-c0065221fa6b` | <https://github.com/identity-md-launches/launch-881-hsxwesxkaamsb0token> |
| 879 | SOS (SOS) | custom_token | `0xd373a9abbc86b7afc4e5ead676b412f74976a622` | `38b076d9-eb5d-4828-a231-6051eb6f5e98` | <https://github.com/identity-md-launches/launch-879-sos> |
| 878 | IMDog (IMDOG) | custom_token | `0xe9a39c7f3c5af1e71dfa1ea3f289473271a4bfd8` | `e6c04c93-4e65-4ce8-9465-e3206422edc2` | <https://github.com/identity-md-launches/launch-878-imdog> |
| 875 | Moss (Moss) | evm_project | `0x47feef4635eea79e95421f77437f0c19ee36ee9e` | `409e0b40-186f-4dd2-8eca-c173d29cf19e` | <https://github.com/identity-md-launches/launch-875-workflow-contract-stage-context> |
| 874 | NumosIMD (NUMOS) | custom_token | `0x89cf6a870ea3aa2392bd01df35eb731a2a72ee7b` | `0e394470-6666-4144-803c-d2f5bbd27c37` | <https://github.com/identity-md-launches/launch-874-numosimd> |
| 870 | Rise (RISE) | custom_token | `0xe1c42c5791425b1c1f6c25bd69815cdf4591b618` | `a7ec8bdd-1404-45fd-9eab-cdc40365644c` | <https://github.com/identity-md-launches/launch-870-rise> |
| 864 | Numos (NUMOS) | custom_token | `0x61c4c8c0d9d060bb0615a507c0ab391d6eeae91b` | `d16fd1c7-606f-4623-af2a-848bbab87c49` | <https://github.com/identity-md-launches/launch-864-numos> |
| 861 | Imd6900 (IMD6900) | custom_token | `0x9d0a5da56f73b6bfe1a73806dd8131c136c44812` | `b88fa149-3e10-4980-86bd-a7a6630bdd52` | <https://github.com/identity-md-launches/launch-861-imd6900> |
| 843 | SwarmInu (SI) | custom_token | `0xe4372e859950cf56a58f972c87e74e1f079dcbdf` | `111eb3bd-3052-434a-93ba-bf65aeed1c4a` | <https://github.com/identity-md-launches/launch-843-swarminu> |
| 839 | ADAM (ADAM) | custom_token | `0xedbafd7dbae2abc3119276814e8b738496edba0c` | `610c9ea8-f60d-4640-bd27-bf91fdaf4548` | <https://github.com/identity-md-launches/launch-839-adam> |
| 836 | Swarm Pepes (SWARMPEPES) | custom_token | `0x2d3f5de0282d0127facdb64ae1bf778981f4aa75` | `da2fb34b-7d44-46ff-a0b2-5efc72357302` | <https://github.com/identity-md-launches/launch-836-swarm-pepes> |
| 832 | KING (KING) | univ4_hook | `0xa160a8305249e3a07bcf8723ca5803b5a2737e8d` | `4154320f-384b-46d9-b178-81b32f838dbb` | <https://github.com/identity-md-launches/launch-832-redeploy-already-built-reviewed> |
| 831 | Identity Units (UI) | custom_token | `0xd2e546680e04e972f6108ebed6627fb097c86217` | `9ba4fb11-538b-44c5-9170-23bf5e59e442` | <https://github.com/identity-md-launches/launch-831-identity-units> |
| 829 | StrataIMD (STRATA) | custom_token | `0xe56b182670503c3bf73e79ca5710c175907a0560` | `4b6fade4-991e-4b19-9745-bcdbf93f382b` | <https://github.com/identity-md-launches/launch-829-strataimd> |
| 824 | AINSEM (AINSEM) | custom_token | `0x4dc25f4a5beecfdd7ef3dde1c250cbcc29497753` | `e0cd6858-1efc-49c3-a809-a0b59098bf13` | <https://github.com/identity-md-launches/launch-824-ainsem> |
| 823 | Pachu (PACHU) | evm_project | `0x05931b5d7c0f5fbb2315a87ed48e3167483b1b67` | `007bd390-94cd-41cf-b262-a82e3cf25e77` | <https://github.com/identity-md-launches/launch-823-pachutoken> |
| 812 | imdUsd (IMDUSD) | custom_token | `0x3190c988b635c28f307687f93d699333fdc3190c` | `0a98bce4-2d50-4d55-ac93-81805c792de7` | <https://github.com/identity-md-launches/launch-812-imdusd> |
| 810 | Pegzeus (PEGZEUS) | custom_token | `0x999a3853ba4305f432ba6d39d9204cca121bf793` | `19c47fd1-08dc-4ffe-8ab8-f35a79283bdb` | <https://github.com/identity-md-launches/launch-810-pegzeus> |
| 805 | StrataIMD (STRATA) | custom_token | `0x5b9aa7a7443964e80045ea9033e5ebf4f44979e4` | `b0e9ae7d-950f-4109-af26-d3aeb8de04a6` | <https://github.com/identity-md-launches/launch-805-strataimd> |
| 802 | Imd6900 (IMD6900) | custom_token | `0x7413073711e68a182567efaf11505c80a1a5761a` | `b27dfe82-8d92-416a-81e8-4d7d637f6409` | <https://github.com/identity-md-launches/launch-802-imd6900> |
| 798 | Identity Units (UI) | custom_token | `0xee74e6ee48c0dc38bb46af59fdff427563ed3c2c` | `b6461d19-78c3-41fc-a7ec-e412b7b202c8` | <https://github.com/identity-md-launches/launch-798-identity-units> |
| 794 | Agent (AGENT) | custom_token | `0x78736d25fb85de6b0bc5835f597f6fee9915d3b6` | `03909fe7-4686-4a96-87f6-8a283363b797` | <https://github.com/identity-md-launches/launch-794-agent> |
| 791 | Slabs (SLABS) | custom_token | `0x73cbf9aaf60bcfa816a703872e5d6e4563eb65bb` | `8418ae03-2cfd-438f-8c12-00ff3b7f6095` | <https://github.com/identity-md-launches/launch-791-slabs> |
| 784 | WIN (WIN) | univ4_hook | `0xd7a712f3b8c574c87b1b2bd1682431093c49dc1c` | `5410a4c1-b4f4-43cf-8271-236481e641c8` | <https://github.com/identity-md-launches/launch-784-custom-token-last-buyer> |
| 780 | HI (HI) | custom_token | `0x4b3d4fa5e6c043cc56651da83bd857a2cc355b01` | `4d0b5f3b-de9f-4178-b9b3-b13240edcd66` | <https://github.com/identity-md-launches/launch-780-hi> |
| 777 | Pepes (PEPES) | custom_token | `0x75652f324aa507cefbcbc321379612d0345d270b` | `3ded4a21-3a73-4039-90e4-04c485db8e5f` | <https://github.com/identity-md-launches/launch-777-pepes> |
| 775 | Ransom for Seat 1376 (FREE1376) | univ4_hook | `0x4543e6b511a9a7a75b56607e27997c987ea05878` | `d6efcda2-d35b-40c0-aef0-6c089a180773` | <https://github.com/identity-md-launches/launch-775-ransom-for-seat-1376> |
| 773 | Pepes (PEPES) | custom_token | `0xa562b9e8c27aeb3f55e1f8bd04bfeabdcdb081e0` | `e8613971-88ce-4e50-8d13-39f3b709b16e` | <https://github.com/identity-md-launches/launch-773-pepes> |
| 767 | Pepes (PEPES) | custom_token | `0x10c930d707e6d83708e69516c8d594be7cfb5654` | `46eccc97-4996-4a69-8ddd-d460dcd18bd0` | <https://github.com/identity-md-launches/launch-767-pepes> |
| 763 | Swarm Local 2000 (STRIKE) | custom_token | `0xd1f91ee80ca01ecedd7bc8172b3441ec8c508286` | `f8b118f2-0e4c-4ac6-b133-a1be76fbe5b6` | <https://github.com/identity-md-launches/launch-763-swarm-local-2000> |
| 761 | Dev Is A Robot (NODEV) | evm_project | `0x0629c60759a8b876de2b4596b58284b36510013c` | `003df701-9569-4a55-acf5-daee223ffdf1` | <https://github.com/identity-md-launches/launch-761-workflow-contract-stage-context> |
| 760 | Why (WHY) | custom_token | `0xf55b01958f805f680cc72b48e022eb80e607d58e` | `0ac8f539-98e3-40f9-8640-682953978e3b` | <https://github.com/identity-md-launches/launch-760-why> |
| 757 | IMD DOG (IMDOG) | custom_token | `0xd189ddeef8827f8fcd9c5c9321191c62ed0f783d` | `1b15d3a1-b515-4f4f-9ec8-eed45ddac56d` | <https://github.com/identity-md-launches/launch-757-imd-dog> |
| 756 | Infinite Money Glitch (IMB) | custom_token | `0x990ad3eccc7874f18464366e7caa893d915b5cdd` | `d64b23f1-2160-4c2e-9e9a-16f374720fa3` | <https://github.com/identity-md-launches/launch-756-infinite-money-glitch> |
| 754 | ID PEPE (PEPE) | custom_token | `0x3b6d536d8adf4335a79d8605b3bcc17160ea56d6` | `3335b52f-fba8-4227-9f0d-46e2ffa98a19` | <https://github.com/identity-md-launches/launch-754-id-pepe> |
| 751 | Infinite Money Dopamine (IMD) | custom_token | `0xf3ca98baf1b9832162198a4e06608418f8c2faf6` | `fb1376c0-522e-4415-ad0d-3099a41bf781` | <https://github.com/identity-md-launches/launch-751-infinite-money-dopamine> |
| 747 | Identity (ID) | custom_token | `0xde1cbe2801ab10162c31aa6dc278bed2b516dc3b` | `2dc5f08d-c901-4691-b7ca-8a7acd921569` | <https://github.com/identity-md-launches/launch-747-identity> |
| 745 | Daemon (DAEMON) | custom_token | `0x4a09888667f7bcf5ff990b213e6e09ac442e24f7` | `4ff2e1ad-0c99-4df7-99fe-3f640ef28024` | <https://github.com/identity-md-launches/launch-745-daemon> |
| 741 | Swarm Made (MADE) | custom_token | `0x821502ef6c3cf75347133d27b99cbf821ec05a9f` | `987c29c7-fc8f-4d77-958d-62dbd860969c` | <https://github.com/identity-md-launches/launch-741-swarm-made> |
| 740 | McLovin.id (MCLOVIN) | custom_token | `0x4122e7952859a2765d88b8ea49f04ee4e152ebc0` | `6b2fe01c-7a65-4075-b6ae-556c4b13cc3b` | <https://github.com/identity-md-launches/launch-740-mclovin-id> |
| 739 | IMD (IMD) | custom_token | `0xaa6b95d6c320b7e6ca9c0edc3eada82f6317da80` | `aa4c9bb5-973d-4aca-9e6d-35ac832612a9` | <https://github.com/identity-md-launches/launch-739-imd> |
| 737 | Zero To One (ZTO) | custom_token | `0xd782bdea4ef02a0bd391eb9089470c8080f0a68e` | `030c609a-ae99-4a2b-9950-2941535ab63d` | <https://github.com/identity-md-launches/launch-737-zero-to-one> |
| 732 | GENESIS PROTOCOL (GENESIS) | evm_project | `0x0e5c9297c9f02af05e691fd5421a73158e27d748` | `c2536a52-a060-4831-bd7c-60d700b9596a` | <https://github.com/identity-md-launches/launch-732-workflow-contract-stage-context> |
| 713 | ADAM (ADAM) | evm_project | `0x9a9d76ff61aaa11344f43915c16c58a7ca04bc42` | `389b403b-32d7-4886-8e9c-abf4fece8037` | <https://github.com/identity-md-launches/launch-713-task-single-job-do> |
| 710 | Guestbook (GUEST) | evm_project | `0xfe3aa5706029b96908c1011cc3260b6abf3d2343` | `a6c74561-0ac3-4d68-8749-ed9cd1211553` | <https://github.com/identity-md-launches/launch-710-fixed-supply-launch-token-plus> |
| 697 | GOTCHI (GOTCHI) | evm_project | `0xfa9b6bda4bca5a8dbba70ef30663078fb7a9b703` | `e5638691-fadc-41a2-9677-208711df175c` | <https://github.com/identity-md-launches/launch-697-gotchi> |
| 684 | IMD Offsets (IMDO) | univ4_hook | `0x22950d52f364093a24c347cc87322ac3ed09d3c7` | `4c5a62a2-9b05-4591-b224-cc4743e05ecc` | <https://github.com/identity-md-launches/launch-684-imd-offsets-token-symbol-imdo-chain-id-1> |
| 639 | BurnTax (BTAX) | univ4_hook | `0x9d6b114ceeffaf645216e33fa9db8e869ebed19a` | `2773731b-934a-4046-a68f-f3a436a1c6d3` | <https://github.com/identity-md-launches/launch-639-burntax-uniswap-v4-hook> |
| 637 | GOTCHI (GOTCHI) | evm_project | `0x195055e3fa69bff7821d7ebe5e688df33f728c35` | `efadba70-d658-4365-9199-7b129d30f257` | <https://github.com/identity-md-launches/launch-637-gotchi> |
| 618 | Frogs of the Swarm (FROGS) | evm_project | `0x14cb616c4cea6ee39f24610fff7090f680262c90` | `1cf2e7f9-e433-4f41-b1f2-4401038e2978` | <https://github.com/identity-md-launches/launch-618-frogs-swarm-turns-every> |
| 616 | Swarm Hackathon Token (HACK) | evm_project | `0x616f48333ea49a9f99c3f7f950389b692312e49d` | `c86dc115-5374-48bb-b2b2-08708a658636` | <https://github.com/identity-md-launches/launch-616-workflow-contract-stage-context> |
| 594 | lumineon (lumi) | evm_project | `0xfe7929e6726350260b99aac04153c33173711272` | `87513a53-cb12-4e4e-9599-293a69a373ac` | <https://github.com/identity-md-launches/launch-594-build-test-independently-review> |
| 579 | Tip Jar (TIPS) | evm_project | `0x0b0e774aaff5ed479d9ff64cfa89b14dd9ae5646` | `6d106ec1-329c-47de-b8a1-01b9ae44fbbb` | <https://github.com/identity-md-launches/launch-579-workflow-contract-stage-context> |
| 578 | Swarm Sticker (STICK) | custom_token | `0x3be16f31508847ef55e66ad0f90a2053dfc73e36` | `b8b18209-fe4e-405c-b13c-ddb0ffdcf119` | <https://github.com/identity-md-launches/launch-578-custom-token-swarm-sticker> |
| 575 | SurfSurf (SURF) | univ4_hook | `0x6c9f29f7115092064d29d7b86d12836494982805` | `549b3d35-f826-44ed-b8c8-447ef984c631` | <https://github.com/identity-md-launches/launch-575-can-buys-only> |
| 571 | OneEthCap (ONECAP) | evm_project | `0xb786bcd955e15909b67a9419f44329c3825d7313` | `fc450805-c268-4424-9f99-c008c96b4a72` | <https://github.com/identity-md-launches/launch-571-contract-accepts-only-eth> |
| 569 | Fare for Medallion 447 (FARE447) | univ4_hook | `0x533f460aa73f47960344c91f6aeef9a8c4e99f5a` | `115cc4c9-8c60-4dba-a842-29c24a6c50d0` | <https://github.com/identity-md-launches/launch-569-take-me-off-road> |
| 566 | Fare for Medallion 447 (FARE447) | univ4_hook | `0xd17c25614f1ff5a67b1549c7a79a46e6a1fdf9d2` | `a1cc43f3-0944-4133-a5b6-33efa52178de` | <https://github.com/identity-md-launches/launch-566-take-me-off-road> |
| 559 | Meme Witness Protection (ALIBI) | custom_token | `0x0239971d4778224f065a1af84d5b157c9ef39a30` | `dd0f56c1-50c5-4ab5-a495-670c4daa47d3` | <https://github.com/identity-md-launches/launch-559-custom-token-meme-witness> |
| 556 | Guestbook (GUEST) | evm_project | `0xfb4ec514a8464a30beccc3b07e2cdd694cbe8e93` | `d2dd2377-07c2-484c-9285-b930e063453c` | <https://github.com/identity-md-launches/launch-556-workflow-contract-stage-context> |
| 555 | Vault Stake (VSTK) | evm_project | `0x03571ed111e77f611b58d3a51e512cc56146d8e8` | `20772bfe-9512-45f2-aae0-807e22da9e39` | <https://github.com/identity-md-launches/launch-555-workflow-contract-stage-context> |
| 553 | Swap Counter (SWPC) | univ4_hook | `0xb86d0e1795480cc66203a4a009d3715ca6ea79d5` | `98e78725-b255-4958-ae4a-978b45d226e8` | <https://github.com/identity-md-launches/launch-553-swap-counter-hook-afterswap-counts> |
| 551 | taxy (t4) | univ4_hook | `0xdc8d03ba7a93e64e616b3ca092d37c5f8d521301` | `fc0ff41d-5f5f-4ddb-967b-a67cc07dac04` | <https://github.com/identity-md-launches/launch-551-uniswap-v4-hook-charges> |
| 549 | Swap Counter (SWAPC) | univ4_hook | `0xb5ff2f4944f4678bfaf7e3eeb9e8f45af42dd8f6` | `24650414-13e6-4a5b-aecf-c747f246f147` | <https://github.com/identity-md-launches/launch-549-swap-counter-hook-afterswap-counts> |
| 544 | Guestbook Token (GUEST) | evm_project | `0xe971af94d7a1619863a1704f4c5164a16be7d7d3` | `6374c1c6-e865-4d4f-bb9c-ba07e39b5320` | <https://github.com/identity-md-launches/launch-544-workflow-contract-stage-context> |
| 543 | SevenDay (SEVEN) | evm_project | `0xc98c785255ef29f690b3b40f71f3d1e313d49d9e` | `5cb14d8c-6d98-4fc1-bb7f-be993ef4df15` | <https://github.com/identity-md-launches/launch-543-workflow-contract-stage-context> |
| 539 | Guestbook Token (GUEST) | evm_project | `0xe0c6962a453de5a2641e8418e2a2cbb261300699` | `bd9e2e0d-054f-4fcf-8744-9a86e908c068` | <https://github.com/identity-md-launches/launch-539-onchain-guestbook-paid-launch> |
| 538 | Launch Token (TOKEN) | evm_project | `0xc3d820e8e82d215b83710c6abbc81976196d1683` | `514c3319-53e8-47c3-9ed8-9942098112f1` | <https://github.com/identity-md-launches/launch-538-vesting-contract-launch-token> |
| 537 | Stake Launch Token (STK) | evm_project | `0x610bc1e7e43d7f1e04e08d1995ffaf23f70362b0` | `a91d2e02-a5d0-4310-a994-8c5af78cc3cc` | <https://github.com/identity-md-launches/launch-537-staking-vault-launch-token> |
| 536 | Taxi (TAXI) | custom_token | `0x1528532a32d7ba320a665797575b5034e9d8802c` | `573fe134-7895-45e5-a076-aec1640314e8` | <https://github.com/identity-md-launches/launch-536-custom-token-taxi-taxi> |
| 535 | Satoshi Test (SATS) | custom_token | `0x7b4b5421b3e0f407e8c5ed0633c30585f084fd92` | `b8e09fc8-e23e-4190-a7a5-8903b3f30249` | <https://github.com/identity-md-launches/launch-535-custom-token-satoshi-test> |
| 534 | Kitty (KITTY) | custom_token | `0x987dd651c0c94fa6e4af5ede1acee0010f1ab94f` | `8ab3a354-8dc9-436d-a50e-eb70e19949e5` | <https://github.com/identity-md-launches/launch-534-custom-token-kitty-kitty> |
| 533 | KITTY (KITTY) | custom_token | `0x21de6ce5addfc889e4670a135f2d9d2114159ccb` | `0a2b659d-8191-4371-95bc-fec0a4bf62e3` | <https://github.com/identity-md-launches/launch-533-custom-token-kitty-kitty> |
| 519 | COMP Launch (CPL) | evm_project | `0xd0fe552dc3aada9ac0e758ca4af985a86fdc488a` | `e92c8d2b-42f2-471b-a573-81b63fe4b897` | <https://github.com/identity-md-launches/launch-519-mockimd-pricefeed-nhifeed-cdpvault> |
| 498 | Swarm Cities (GRID) | evm_project | `0xdcd861b115064c3f85be0ee3ba9b80bd05ae65a5` | `0cd531be-382f-4c0b-8954-498d68c047c6` | <https://github.com/identity-md-launches/launch-498-workflow-contract-stage-context> |
| 495 | PepeJackpot (PJACK) | evm_project | `0xc43fbdcebf6a52d0249270718437603153b684d8` | `f5dae2d0-cbb9-4e40-b54c-62a73a3e746a` | <https://github.com/identity-md-launches/launch-495-workflow-contract-stage-context> |
| 487 | Milestone (MILE) | evm_project | `0x8a962be605ec00381818484b2fd7dee0af78da24` | `196e491c-2bb2-48e0-839a-034bc4a153bb` | <https://github.com/identity-md-launches/launch-487-workflow-contract-stage-context> |
| 483 | Great Family (GFAM) | evm_project | `0xddddebad7fb5a6ab35232df717a55ece0e70630d` | `2173021b-03eb-48e4-aa29-47e52d97d79c` | <https://github.com/identity-md-launches/launch-483-workflow-contract-stage-context> |
| 458 | COMP Launch (CPL) | evm_project | `0xa850f31f678a7bb91b5f6d7da2d0eacb40b585b5` | `99abf4b8-1462-4136-a6c4-b75d6a3cbd76` | <https://github.com/identity-md-launches/launch-458-mockimd-comptoken-mockworkoracle-cdpvaul> |
| 445 | IdentityMD (IMD) | evm_project | `0x10a7117e2f6d89afe15fa8adbc965d7e1c78613f` | `a36cb67d-208f-4149-a31a-4a55cac4833c` | <https://github.com/identity-md-launches/launch-445-workflow-contract-stage-context> |
| 444 | Pact (PACT) | evm_project | `0x7f88ad727adeb8fc70fd198f2d2319349846818c` | `964a1cdf-8b2b-46b7-a327-6e5ef3e7625b` | <https://github.com/identity-md-launches/launch-444-workflow-contract-stage-context> |
| 437 | Heirloom (HEIR) | evm_project | `0xc9f4f32305ff4ef4c87deaa528dd8809a1793c24` | `80fbf0ff-0ef1-4603-9351-9a626b87b2e0` | <https://github.com/identity-md-launches/launch-437-heirloom-crypto-inheritance-vault> |
| 434 | Bitcoin Cooler (BCLR) | evm_project | `0x83efb3848df1bebe203e350d517f4ce7863c8f0c` | `773dc1e8-df55-4a33-9d65-8d119a88d7a0` | <https://github.com/identity-md-launches/launch-434-https-explorer-imd-fun-jobs-9df471c0-b9f> |
| 429 | StakeLaunch (STL) | evm_project | `0xc43f348c986f35a3b64505d435082151d07862a0` | `fea3a2a2-6535-4eae-944b-0598e3ca6687` | <https://github.com/identity-md-launches/launch-429-original-request-build-fixed-supply> |
| 426 | The Room (ROOM) | evm_project | `0xf28caeef077a02824c2f1f3b9bd26275079f55df` | `01479536-860f-40ea-bfa5-79eace1533ef` | <https://github.com/identity-md-launches/launch-426-room-part-2-6> |
| 425 | The Room (ROOM) | evm_project | `0xe9dd00532de533a606cec9e3138a39441abdcadc` | `a47f8c51-7511-44bc-8164-3313f1c3088e` | <https://github.com/identity-md-launches/launch-425-room-part-1-6> |
| 421 | SwarmWorld (SWARM) | evm_project | `0x7a8eff456e76ceea4802be6c09577c7f7838c7d2` | `7a1d5e09-e873-4562-ab36-8ee94e8f91fd` | <https://github.com/identity-md-launches/launch-421-build-swarmworld-core-one> |
| 419 | Allowlist Claim (ALLOW) | evm_project | `0xaaff231346d5ec19868822d0f870a9fa03b2169a` | `c82ec289-1bfd-4dc3-b22f-f2f769b5bb66` | <https://github.com/identity-md-launches/launch-419-allowlist-claim-small-value-free> |
| 376 | CallBook (CALL) | evm_project | `0x635bfc6693424dfe83105fd2947fa9dc87a7a442` | `4befc1a8-008b-40b6-ac69-39de9ffc0a16` | <https://github.com/identity-md-launches/launch-376-callbook-on-chain-tamper-proof-track> |
| 359 | Draw (DRAW) | evm_project | `0xf5b6e3236ee84165b632eb97f9e1454dfd697701` | `c6c2b1f5-7a27-44f2-9dd6-1287a9fbf034` | <https://github.com/identity-md-launches/launch-359-blockhashlottery> |
| 358 | Blockcap (BCAP) | univ4_hook | `0x719e71f67c46c736885e412b41973edf4452150d` | `cd74e008-6a11-47be-b242-012cc4529697` | <https://github.com/identity-md-launches/launch-358-blockoutflowcaphook> |
| 357 | Soapbox (SOAP) | evm_project | `0xb7441f29c2e22dfc83f77d9e59686262476a9259` | `32fb029e-ae9a-4882-b053-049091c3369a` | <https://github.com/identity-md-launches/launch-357-soapbox> |
| 352 | Stoploss (STOP) | univ4_hook | `0xc994fb47592e20d7002f4f41a4e187c3f2705d91` | `69eb7948-b4ef-4d21-96b2-81500f63c7fb` | <https://github.com/identity-md-launches/launch-352-stoplosshook> |
| 351 | Sponsor (SPON) | evm_project | `0xacdd5b18610efdff1db8745f9a1c6f4afc377900` | `3e90cff7-f2f1-4277-a32a-ed0765d86433` | <https://github.com/identity-md-launches/launch-351-daemonsponsorpool> |
| 347 | Allowlist (ALST) | univ4_hook | `0x2015a8219170ab3a182b04eb3aec5c03d90d8ed9` | `a2f8eb8f-f043-4662-8083-60c2dc62e45d` | <https://github.com/identity-md-launches/launch-347-allowlistlaunchhook> |
| 346 | Piggy (PIGY) | evm_project | `0x45f5bc74c61718d49225b54ec12a78714a7beecb` | `4b813316-a6c2-4717-ac06-bfbf8dfbe223` | <https://github.com/identity-md-launches/launch-346-donationvault4626> |
| 342 | Band (BAND) | univ4_hook | `0xd79607176c790725cac9cb886edca9ccb50a64b8` | `c45efa2f-90a1-46e8-b974-1ef96ca0621c` | <https://github.com/identity-md-launches/launch-342-pricebandhook> |
| 341 | Trickle (TRKL) | evm_project | `0x2e5110f8a8826d40718d6f65674ad2309a4f5a67` | `cad40951-4d01-4a3f-8be0-049fcb10c2f7` | <https://github.com/identity-md-launches/launch-341-ethstakingrewards> |
| 329 | Gas Tax (GASP) | univ4_hook | `0x2c30bf926f3c484f87e59401db46b464ed4fd2c4` | `57cd5b76-bee9-4eeb-9521-e04a1aa1e6f2` | <https://github.com/identity-md-launches/launch-329-gaspricefeehook> |
| 324 | Invite (INVT) | evm_project | `0xcec7717d01ae80eea14c93a5631a13b931ec3fed` | `e36a4566-5869-49c7-86d3-43b7752f8b00` | <https://github.com/identity-md-launches/launch-324-referrallist> |
| 322 | ETH Fee (ETHF) | univ4_hook | `0xcb4e7bdceb4d71dd5ce9a8451761acc1105a707c` | `618f53d9-2b8f-4306-bd52-615161bda6d5` | <https://github.com/identity-md-launches/launch-322-ethonlyfeehook> |
| 321 | Guild (GILD) | evm_project | `0x11c1add8e0dd220294837fbf0fc65bdca75cc673` | `98c3ec61-53c1-419e-bcea-bb4f0f9b1e1a` | <https://github.com/identity-md-launches/launch-321-guilddues> |
| 319 | Pawn (PAWN) | evm_project | `0x9f563e0d1a03ea9bc7ec143652e59fc14f70b2a5` | `6f71f445-55e7-457b-a12d-248b9379afc6` | <https://github.com/identity-md-launches/launch-319-nftpawnshop> |
| 318 | JIT Guard (JITP) | univ4_hook | `0xf2eedcab10337316d0964a017b2ff7f29bd199c6` | `92ed5d7a-35dc-4e8f-b962-ad6bbe83d23b` | <https://github.com/identity-md-launches/launch-318-jitpenaltyhook> |
| 315 | Nosandwich (NOSAND) | univ4_hook | `0xa26a6de1daf41775daee351cf4bc10a35f7bf2b3` | `e628af2f-8e98-495a-8ed9-39bc5d657282` | <https://github.com/identity-md-launches/launch-315-antisandwichhook> |
| 314 | Pocket (PCKT) | evm_project | `0xc43a3aabf54bcf17017e089032def50e1734303d` | `7c10d31c-b637-45e4-8c86-b87c81e33ccd` | <https://github.com/identity-md-launches/launch-314-allowancewallet> |
| 310 | Whale Tax (WHAL) | univ4_hook | `0xfe00cb1154a70ddc6276de8b8f16fd5d747248ae` | `543763e2-628b-4091-93d9-2fb043124609` | <https://github.com/identity-md-launches/launch-310-whaletaxhook> |
| 309 | Checkin (CHKN) | evm_project | `0xd758416845f173467513389797c41e800a8e15ec` | `77597ed4-466f-47a9-8daa-d6fd57c5d276` | <https://github.com/identity-md-launches/launch-309-eventcheckin> |
| 301 | Breaker (CBRK) | univ4_hook | `0x7f2ed4fdd432222bdc70d4c00903457eda378168` | `00b25984-d932-4bf4-a97b-5a725e929c73` | <https://github.com/identity-md-launches/launch-301-circuitbreakerhook> |
| 299 | Tranche (TRNC) | evm_project | `0x31a6f0ee61d3f773b3e047d77dba0631b81d5cd0` | `1cbd2564-52c1-46a7-acb1-1c85de90811b` | <https://github.com/identity-md-launches/launch-299-milestonefund> |
| 297 | Lockvote (LVOT) | evm_project | `0x58e0474edf328b5d8e0fdb1a7c22aedfc49c5145` | `cbd827e2-0e85-416a-be08-76116db1510d` | <https://github.com/identity-md-launches/launch-297-lockvotetreasury> |
| 296 | Maxtx (MAXT) | univ4_hook | `0x1a9ec1090618c482723cb4a0dc981511b8b1c4dc` | `8f66e2dc-7535-4b88-ac9a-1323bf7e9533` | <https://github.com/identity-md-launches/launch-296-maxtxhook> |
| 294 | Lease (LEAS) | evm_project | `0x7508156ff9d231217ff507205e4fe41ef42aa120` | `333530b9-5541-4a65-a15b-917337c9e759` | <https://github.com/identity-md-launches/launch-294-rentablenft> |
| 293 | Snipeproof (SNIP) | univ4_hook | `0xcd1f5069fd28049469a5eb521a19a7e61dabfc6e` | `88a24c46-85d8-46f7-8055-9dff66cdbf41` | <https://github.com/identity-md-launches/launch-293-antisniperdecayhook> |
| 291 | Rebate (RBTE) | univ4_hook | `0x18e5b84e2bf2427b4c236e639527af3904bc4689` | `89d0c5ad-35f2-4d97-9dfc-ab8059926c84` | <https://github.com/identity-md-launches/launch-291-lpdonatehook> |
| 290 | Gradients (GRAD) | evm_project | `0xad48cbc311b9d5af8ea0e07bcf43238884af1385` | `f7b9a75f-bb47-4d25-be73-661b199fadef` | <https://github.com/identity-md-launches/launch-290-gradientnft> |
| 288 | Badges (BDGE) | evm_project | `0xa051b89066e7e47e3117c75aabc348d18da386e3` | `521056e2-7f31-40b2-bbb4-486fb89c2ad9` | <https://github.com/identity-md-launches/launch-288-soulboundbadges> |
| 287 | Points (PNTS) | univ4_hook | `0x718f5354974e2947047f353a65b000a61b75fbf2` | `a670be06-3cf0-4e6c-8203-e99c7e2b4442` | <https://github.com/identity-md-launches/launch-287-swappointshook> |
| 285 | Heads (HEDS) | evm_project | `0xad7f3b99f66522149514f582f7a7a97a603cda0a` | `b44cd52c-b642-4cd7-bccb-d6766d3699cf` | <https://github.com/identity-md-launches/launch-285-commitrevealcoinflip> |
| 284 | Candles (CNDL) | univ4_hook | `0x5845f623771593af103d486e451353d9355caaeb` | `fbed9a85-d733-4ebc-bcef-b3c64f494b96` | <https://github.com/identity-md-launches/launch-284-ohlccandlehook> |
| 282 | Noughts (NGHT) | evm_project | `0xe0d98c90d2cb2507b36d1fd104f110a80a07d9dd` | `14ab260c-c63f-40c2-b1c4-8dbc94c39f89` | <https://github.com/identity-md-launches/launch-282-tictactoewager> |
| 281 | Swap Tip (STIP) | univ4_hook | `0x86a20b901f1e5082a4bea46045e3a05298784181` | `170567d8-9a8e-41ed-9072-672fb141c11c` | <https://github.com/identity-md-launches/launch-281-swaptiphook> |
| 278 | Oddsmaker (ODMK) | evm_project | `0x79c1fc6ad772e720c0d85688e49c94013c6ef087` | `6e8f164e-05f8-4d77-868b-391b331248a6` | <https://github.com/identity-md-launches/launch-278-parimutuelmarket> |
| 277 | Farm (FARMX) | univ4_hook | `0xc8b269a25a65a54fb193f7737ddb9dc386dc5a88` | `3d1c8c28-4716-4043-bc32-5e5a7a4f0ee1` | <https://github.com/identity-md-launches/launch-277-liquiditymininghook> |
| 275 | Tiers (TIER) | univ4_hook | `0xb0d54e89c5a7888446c1ab93f12ace3054c847c7` | `a9c431b4-53b9-4eba-b85a-e287fc9e784e` | <https://github.com/identity-md-launches/launch-275-loyaltytierhook> |
| 274 | Match (MTCH) | evm_project | `0xb5e8632a4d35a4bd206c5f0c4145c39f5c3cf5a2` | `b3674ee7-4c71-4392-a1c3-aff0638292e7` | <https://github.com/identity-md-launches/launch-274-quadraticfunding> |
| 273 | Threeway (THRW) | univ4_hook | `0xcab76e4548776e3232853ab65c09f5ec2914bbdc` | `1923a978-6539-4e4f-8b0b-ffc102e68144` | <https://github.com/identity-md-launches/launch-273-feesplithook> |
| 272 | Taskboard (TASK) | evm_project | `0xbd6b348c9ea02447f5f6af556de42647a16a3019` | `43c0104e-fc33-4a44-8937-bacddc6f58da` | <https://github.com/identity-md-launches/launch-272-swarmjobboard> |
| 270 | Kudos (KUDO) | evm_project | `0x4a64f2baeb7fafca2c023cbd8a5f3898649d3c2c` | `58cb99e6-81cb-4e25-9bf8-ef841ed577df` | <https://github.com/identity-md-launches/launch-270-kudosepochs> |
| 268 | Oneway Launch (OWLN) | univ4_hook | `0x6962c22809a04681907e7f7e0281879900d5f0be` | `d2e637f2-10d7-48d9-90e7-9db146088506` | <https://github.com/identity-md-launches/launch-268-buyonlywindowhook> |
| 267 | Pyre (PYRE) | evm_project | `0xe6b240d60de634b646e5b3693782d6df2c81a278` | `1b579f1c-7cb8-4dfa-ab60-fa9b4f140810` | <https://github.com/identity-md-launches/launch-267-burnleaderboard> |
| 265 | Ticket (TIKT) | univ4_hook | `0x2697a540c5c65fb4b028a370560ef0b31ccdd7fe` | `537a433a-fab7-4103-9860-90d08308560c` | <https://github.com/identity-md-launches/launch-265-swaplotteryhook> |
| 264 | Doomsday (DOOM) | evm_project | `0xbb794a028d8c2b978520917e36d07670358d8c88` | `6d04ceb6-b353-42fa-9fa0-f02e8b532ee0` | <https://github.com/identity-md-launches/launch-264-doomsdayclock> |
| 262 | Referral (REFR) | univ4_hook | `0x9ff30d1afa005742830f2f78a9412f0aa8fff409` | `04c05210-7ad2-47a9-b22a-5dc9b52ce28a` | <https://github.com/identity-md-launches/launch-262-referralhook> |
| 261 | Streak (STREAK) | univ4_hook | `0xe2f5bd563be004f9b366c0a98a3ecef6b727c1f7` | `fdad2410-2205-44a7-8290-c4d020b9da2a` | <https://github.com/identity-md-launches/launch-261-buystreakhook> |
| 260 | Escalation (ESCL) | evm_project | `0x219fca9064527e9773cd4b49798502774490f1e8` | `77a01da6-b966-458d-847b-763ec6c7ba46` | <https://github.com/identity-md-launches/launch-260-dollarauction> |
| 258 | Oneway (ONEW) | univ4_hook | `0x52e1a5d1257fe87c8a7aae7094ba2e6ad2d0253f` | `dba466f8-9df5-4742-9099-da3a12fe931d` | <https://github.com/identity-md-launches/launch-258-asymmetrictaxhook> |
| 257 | Desk (DESK) | evm_project | `0xece5c9e8705a8175ac9c7cfd4ec596b791e48aa5` | `27d2d367-9414-4352-bc9d-a5d3c028fd52` | <https://github.com/identity-md-launches/launch-257-otcboard> |
| 255 | Lockup (LKUP) | univ4_hook | `0x60ded28773fd684c6940d747805992f1bf6e2a9c` | `d5b8e88d-b8c0-4757-a567-89a4f008b818` | <https://github.com/identity-md-launches/launch-255-liquiditylockuphook> |
| 254 | Drip (DRIP) | evm_project | `0xcacf5fc6c177d1147ed1c44aa86295c5edd94df3` | `418e6c15-929b-4625-abf4-726dea2378e1` | <https://github.com/identity-md-launches/launch-254-tokenfaucet> |
| 253 | Volume (VOLM) | univ4_hook | `0xf7047a8492fe4d9db3a85ad9942b51e0e195225e` | `04ac0b4c-e623-4522-9989-3a6997f0846f` | <https://github.com/identity-md-launches/launch-253-volumeleaderboardhook> |
| 251 | Billboard (BILL) | evm_project | `0x6b9141aceec34cc852eb495284ea46ccb210d2a6` | `d36ec7ed-8461-4a69-8e70-f964d65d6919` | <https://github.com/identity-md-launches/launch-251-harbergerbillboard> |
| 250 | Receipts (RCPT) | univ4_hook | `0x7603ee0f4346b9118c5474311196195d5ecb4c6e` | `d6bd324d-f1b1-4394-b215-595c20425405` | <https://github.com/identity-md-launches/launch-250-swapreceipthook> |
| 248 | Circle (CIRC) | evm_project | `0x86241a289dd98beb222d4770eea740cbd46a9145` | `832f7a44-cde0-4cf2-be94-8b3a9f565d98` | <https://github.com/identity-md-launches/launch-248-savingscircle> |
| 247 | Takeprofit (TKPF) | univ4_hook | `0x67218a97ccfffe56cb07c786a29fab4c86ebc45e` | `06be26db-a8ac-44fd-89a0-3be8532d8ee0` | <https://github.com/identity-md-launches/launch-247-takeprofithook> |
| 245 | Geomean (GEOM) | univ4_hook | `0xcd04aa75d52e36482548d20d7eb5942c98eef9c6` | `6ca29016-f690-450d-be48-020824900bf6` | <https://github.com/identity-md-launches/launch-245-geomeanoraclehook> |
| 244 | Heartbeat (BEAT) | evm_project | `0x147ee1ea6dff20feb227151fef4c5d41d46f2dd2` | `f84877c1-85ef-4815-9ad7-f827272adcef` | <https://github.com/identity-md-launches/launch-244-deadmansswitch> |
| 242 | Keyring (KEYR) | evm_project | `0xa57baadbc485722359c7dfc44916343c5a7c15e4` | `30dca88c-ecc1-45ab-8f79-4bb0d3954025` | <https://github.com/identity-md-launches/launch-242-keyringmultisig> |
| 241 | Last Buyer (LBUY) | univ4_hook | `0x0db82f38997c2ab9cff32e4fdc41c41fa4d1a318` | `e29039eb-2fa3-4570-bdbf-3a228fed2b31` | <https://github.com/identity-md-launches/launch-241-lastbuyerjackpothook> |
| 239 | Ratelimit (RATE) | univ4_hook | `0x14ca885130e76c69ba66e8bf79aa587753623eb4` | `fb56b990-1abf-4252-b81f-460ea366728a` | <https://github.com/identity-md-launches/launch-239-swapratelimithook> |
| 238 | Gavel (GAVL) | evm_project | `0xc3006d2080537c453a661d6760d54233c8917c85` | `8595d95c-9033-4d7d-b141-a7d3423a5d24` | <https://github.com/identity-md-launches/launch-238-lotauction> |
| 237 | Happy Hour (HAPY) | univ4_hook | `0xd99b05f7a322d7c11a358416fcd0279bfa7adc02` | `f61dea12-1936-4851-8e83-ff37328e996d` | <https://github.com/identity-md-launches/launch-237-happyhourhook> |
| 236 | Momentum (MOMO) | univ4_hook | `0xf850bc356ea61a7623f2b5620648e51c9b4908a4` | `a6a76768-571d-43cd-9391-710ba12a3380` | <https://github.com/identity-md-launches/launch-236-momentumfeehook> |
| 235 | Ember (EMBR) | univ4_hook | `0xd5f01c3b271e89e1508a20bf46cc1cd7d1cf98d6` | `07bd8e80-6bd6-49a9-b4f4-7d724d47b23f` | <https://github.com/identity-md-launches/launch-235-buybackburnhook> |
| 234 | Kickoff (KICK) | evm_project | `0xdc68769578dc288131fe1cf663ac618bb3a0c887` | `37b69e5a-dbf6-4bdd-a513-5f9fbd60a39c` | <https://github.com/identity-md-launches/launch-234-crowdfundcampaigns> |
| 233 | Crown (CRWN) | evm_project | `0x4ec36a35e2eb384d324961c629344067b47d3cd4` | `81721fbd-ff99-4239-a26b-c5840c42e21c` | <https://github.com/identity-md-launches/launch-233-kingofthehill> |
| 232 | Arbiter (ARBT) | evm_project | `0xd10a0e1f765315d471c175a2a581965385206132` | `fc0c4b51-8812-418c-835a-58ce0b8bf892` | <https://github.com/identity-md-launches/launch-232-arbiterescrow> |
| 231 | Holder Discount (NFTD) | univ4_hook | `0x0a7e5114d4007b4b5196fdf0c8697c4e569bf8d8` | `99c1d6ab-a6d3-4cde-99c6-bf2af466c499` | <https://github.com/identity-md-launches/launch-231-nftholderdiscounthook> |
| 230 | Pixel Wall (PIXL) | evm_project | `0xeb31f50280793b2825a940b37b4294d86b0909d3` | `0ac37315-248f-49a3-b0ae-6087acd07c31` | <https://github.com/identity-md-launches/launch-230-pixelcanvas> |
| 223 | Happy Hour (HAPPY) | univ4_hook | `0x254ceee03c7c96ed570b4152874957215a0aa1b3` | `11dcb245-052f-4ae9-900c-ea8537a14404` | <https://github.com/identity-md-launches/launch-223-happy-hour-uniswap-v4> |
| 222 | Parcel (PRCL) | univ4_hook | `0x8376b75b1c0f3a80728c9d8fdd0d03e84458aa58` | `a95bdc2c-e8f6-4815-9575-a0774646a8ca` | <https://github.com/identity-md-launches/launch-222-pass-parcel-uniswap-v4> |
| 220 | Pairwise (PAIR) | evm_project | `0x9cfe88a35c51e5efd28bc77372706147a6301f3a` | `d82e2055-1b75-4667-83c6-97c66edf93da` | <https://github.com/identity-md-launches/launch-220-trustless-nft-transfer-escrow-system> |
| 205 | Priority Queue Launch Token (PQL) | evm_project | `0x8949335be9008402423912abd97ff5d1e6646af5` | `6db093ab-243f-460e-b2a5-4111a3c804bb` | <https://github.com/identity-md-launches/launch-205-build-bounded-queue-most> |
| 186 | pepes ice (ICE) | univ4_hook | `0xb0bb5c62c2cbff432a0377a0a8b71d1775de77c8` | `5af340ea-6022-40a8-b2c0-861d59a51fff` | <https://github.com/identity-md-launches/launch-186-pepeice-jackpothook> |
| 183 | pepes ice (ICE) | univ4_hook | `0xf3dab52ca75b7abeb31ecd0136b01a45a5c48f37` | `a233e4b7-77a9-4d3c-a01f-a0d820127302` | <https://github.com/identity-md-launches/launch-183-pepeice-jackpothook> |
| 177 | Oracle Challenge Test (OCTEST) | evm_project | `0x980f3004cb0149d6713837aa250f1c3e3753a5ac` | `d1175e1d-2c3c-4a9d-bd20-c9347f680801` | <https://github.com/identity-md-launches/launch-177-oraclechallengetoken-imdoracledisputereg> |
| 170 | Fare for Medallion 447 (FARE447) | univ4_hook | `0x4ced114edef2d3b0a46d0a8c206edea3729d5a50` | `5c58019b-eb23-481b-889f-2356c8e92e1c` | <https://github.com/identity-md-launches/launch-170-take-me-off-road> |
| 168 | TOLLGATE (TOLL) | univ4_hook | `0x03d052d94bb8160f68f0658ecdbfd454b4e6327b` | `bca9ad82-76c5-466b-93f0-3336108c6d68` | <https://github.com/identity-md-launches/launch-168-release-tollgate-symbol-toll> |
| 167 | Sealed Pixels Token (SPXL) | evm_project | `0xddfacbc751847e034d7742dfd6910f284915b613` | `7461d3ce-0fc4-47ac-a3af-59312eaff786` | <https://github.com/identity-md-launches/launch-167-build-test-adversarially-review> |
| 153 | Seat Compute (COMPUTE) | evm_project | `0x3a7fd75f1ba7f1683e206e048e399d452901426b` | `26f496cb-eb56-4190-982f-431a5a740b71` | <https://github.com/identity-md-launches/launch-153-workflow-contract-stage-context> |
| 149 | Noop Hook Token (NOOP) | univ4_hook | `0xadd625bfb7cdbc09ae817c4932d9072595113152` | `c03586f4-42cb-46e3-a6a5-d39619a68a25` | <https://github.com/identity-md-launches/launch-149-workflow-contract-stage-context> |
| 148 | Counter Test (CNTR) | evm_project | `0x6a823925da61c747395d134e6dea733cc6a4064b` | `bce7e9c8-af3a-45e2-9efb-c3109cf807c1` | <https://github.com/identity-md-launches/launch-148-workflow-contract-stage-context> |
| 145 | Membership Club Token (MCLUB) | evm_project | `0x68da2f693376d9d25f3c6070fba37e33f78b6bcc` | `84af6f4c-a5ab-4bbe-a6e4-a5617367f62e` | <https://github.com/identity-md-launches/launch-145-workflow-contract-stage-context> |
| 139 | Pepe Values Pepe (PVP) | univ4_hook | `0x55d833403ba3ef446074902946fe4d6b7fe4ce56` | `f4249894-a729-4123-880c-91fd39224e00` | <https://github.com/identity-md-launches/launch-139-workflow-contract-stage-context> |
| 124 | v4-burn (V4BURN) | univ4_hook | `0xe3603e321165d0250e5319ff6d3cd5023b0a7258` | `b2ab92a7-3968-4090-9678-ee739ecbd0f7` | <https://github.com/identity-md-launches/launch-124-workflow-contract-stage-context> |
| 114 | Mini Swap (MSWAP) | evm_project | `0x63604976838c62e6d3e544f5cda2b14e4a430725` | `f3ba1e08-2fb2-484f-a905-442561eea8c8` | <https://github.com/identity-md-launches/launch-114-miniswaptoken-minipair> |
| 113 | Time Lock (LOCK) | evm_project | `0x1befeab42d891b69441405a676de77565619e084` | `1d2a6994-2ece-43b8-8429-63e1e08c5e7b` | <https://github.com/identity-md-launches/launch-113-timelocktoken-timelockbank> |
| 112 | Tip Jar (TIPS) | evm_project | `0x75a4fd4a73a8d9be8e050f9e9a3e5065f22b31fd` | `15bd34ab-1fb2-4166-a010-c539d7d51656` | <https://github.com/identity-md-launches/launch-112-tipjartoken-tipvault> |
| 108 | Proof Of Work (WORK) | evm_project | `0xee85b80543c4f301b33505de4d9d0217ce26d8dd` | `ee1f32a2-7f0e-48f1-88c2-1c591e0bdc66` | <https://github.com/Identity-md/launch-108-proofofworktoken> |
| 92 | Cliffhanger (CLIF) | evm_project | `0xe8ae910bbabf4a8ea92b954dab364d106c34a224` | `57b612f0-cd80-4945-8744-18f0c57bbc0a` | <https://github.com/Identity-md/launch-92-workflow-contract-stage-context> |
| 91 | Wager (WGR) | evm_project | `0xc4780c45097a850ea3880dd6062efe447ac295fb` | `3b9a04ef-dbbe-455e-bd77-4be18d60aa44` | <https://github.com/Identity-md/launch-91-workflow-contract-stage-context> |
| 90 | Pledge (PLDG) | evm_project | `0xe2f3b168b54adc238dd62d318a55ddb0c2980868` | `b307b17c-75d1-4673-aa93-2dcd31f91bb2` | <https://github.com/Identity-md/launch-90-workflow-contract-stage-context> |
| 89 | Conduit (CNDT) | evm_project | `0x68311151c0b895c65d7cc16ad6c6b5bad689d4a4` | `010e165a-20cd-4bce-aeab-59321910e276` | <https://github.com/Identity-md/launch-89-workflow-contract-stage-context> |
| 88 | Handle (HNDL) | evm_project | `0xf925ebb0ef25dd36b86007683154b549c3dae8e9` | `db663cb4-5b7b-423c-be1d-a8131715bd36` | <https://github.com/Identity-md/launch-88-workflow-contract-stage-context> |
| 87 | Cadence (CDNC) | evm_project | `0xc4c95fee607301105102c812bb0e70e593006479` | `85ea44b4-5c75-4e69-9f72-c5434c0841ed` | <https://github.com/Identity-md/launch-87-workflow-contract-stage-context> |
| 86 | Raffle (RAFL) | evm_project | `0xeb86b6e8bc2b73726f26f7a4da58ada9909b9512` | `fd77b4ce-b76e-4151-a73f-9b66fd613b7d` | <https://github.com/Identity-md/launch-86-workflow-contract-stage-context> |
| 85 | Lastlight (LAST) | evm_project | `0x56bfa1c48957e6c7cfed1dd1fd88917f74d2ba9b` | `09cf9ad6-f297-4fa4-a772-8cd13af78f11` | <https://github.com/Identity-md/launch-85-workflow-contract-stage-context> |
| 84 | Commons (CMNS) | evm_project | `0x77f62df1282ac4acc620aa4fd5d9fa1114be5d7c` | `aa73dbed-bff6-45f2-b95a-d74329d32667` | <https://github.com/Identity-md/launch-84-workflow-contract-stage-context> |
| 83 | Descent (DSNT) | evm_project | `0xd2cc2f3dc2e3c321c7ec1fb9623ff71544694216` | `0352d62b-412a-497a-8dc3-c2babb0ce7c6` | <https://github.com/Identity-md/launch-83-workflow-contract-stage-context> |
| 82 | Handshake (SHAKE) | evm_project | `0x1423dc0944a33c7e2f2939b338c659fc6c959569` | `4f25cf94-e658-4208-98df-62fccd482804` | <https://github.com/Identity-md/launch-82-workflow-contract-stage-context> |
| 81 | Quorum (QRM) | evm_project | `0x337583b9cb98e04288aac10046156dde0715f4ad` | `76e03efb-fd31-47ed-a254-8eedf1bacf07` | <https://github.com/Identity-md/launch-81-workflow-contract-stage-context> |
| 80 | Splitwise (SPLT) | evm_project | `0x6e10b801edf8296afa4584f6fafe5426f2a48169` | `217be56c-a7d6-46d3-8f57-78fc1f6e1f50` | <https://github.com/Identity-md/launch-80-workflow-contract-stage-context> |
| 79 | Timebox (TBOX) | evm_project | `0xaeb152fd4089562c44c2b46d75fd4d6f707d8d5d` | `00ce6ffd-c91b-4c46-8936-590ee409cf51` | <https://github.com/Identity-md/launch-79-workflow-contract-stage-context> |
| 78 | Streamline (STRM) | evm_project | `0x28626a828c708f0eade7980f40ece0c328999e63` | `9a7dab78-e3bb-4661-a457-53df8dd4c0b3` | <https://github.com/Identity-md/launch-78-workflow-contract-stage-context> |
| 62 | Stream (STRM) | evm_project | `0x98aed11946ced443b1fc996f2876a5b3e9c0be8f` | `30b68d1c-5aee-4e66-938a-643b8e31da7b` | <https://github.com/Identity-md/launch-62-build-independently-review-streaming> |
| 61 | Escrow (ESCR) | evm_project | `0x66215662ca880b36de64fb799c3815ae8505ddbb` | `1237279a-e94d-4e58-9c90-55f39ce73c91` | <https://github.com/Identity-md/launch-61-build-independently-review-two> |
| 60 | Guest (GUEST) | evm_project | `0xc6a239c35f3b90e0eb2b33e7949b6135410211ee` | `e21ad4ec-5fc5-475e-a797-165fad558b47` | <https://github.com/Identity-md/launch-60-build-independently-review-guestbook> |
| 59 | Vote (VOTE) | evm_project | `0xf78868e0b430a1d4679982097bbfc315792551bd` | `239179df-bd43-4bf4-94ea-4bff376a6f1e` | <https://github.com/Identity-md/launch-59-build-independently-review-token> |
| 58 | Bounty (BNTY) | evm_project | `0x3634eb085e52caa4a330dc60afca8f93c0696ead` | `2aaf30a8-c182-43e0-a2ed-5e4a67738693` | <https://github.com/Identity-md/launch-58-build-independently-review-bounty> |
| 57 | Bid (BID) | evm_project | `0x050d11b58ec5db886f0ae611c0c5eca0ac573948` | `d7473650-915a-43a8-95f2-e2bbcb09a0f5` | <https://github.com/Identity-md/launch-57-build-independently-review-sealed> |
| 56 | Stake (STK) | evm_project | `0x8fa3cfd90988208f091297cc3d3714ad1f222a2c` | `359e264a-8381-466d-bd3e-3bd18c696340` | <https://github.com/Identity-md/launch-56-build-independently-review-simple> |
| 55 | Vest (VEST) | evm_project | `0x940ee4bbfd902dc82c34b27ceb3774b25b3aa2c0` | `379c4ae3-0c26-4255-a185-39b49919f853` | <https://github.com/Identity-md/launch-55-build-independently-review-linear> |
| 54 | Lock (LOCK) | evm_project | `0x8b73f217a8261c3373e84b2966e10126b531aa5c` | `e696aa9d-d5b2-4823-9ced-540f2f0e4823` | <https://github.com/Identity-md/launch-54-build-independently-review-time> |
| 53 | Tip Jar (TIPJ) | evm_project | `0x09565c77d7e6e786e0acde4ed506eb48ae79661c` | `2e900734-2353-49a4-a21f-1db5375c19f3` | <https://github.com/Identity-md/launch-53-build-independently-review-tip> |
| 51 | High Roll (ROLL) | evm_project | `0x1eb463ff9a7868b05734f42548c593cce5c1f4bb` | `8b853906-a016-40e5-8ba5-81b37f138ed4` | <https://github.com/Identity-md/launch-51-workflow-contract-stage-context> |
| 50 | Odds and Evens (ODDS) | evm_project | `0x7e31f1b1833197c598e280212886ccd363f7f8c0` | `6406286f-2242-4f75-b672-4982617d7160` | <https://github.com/Identity-md/launch-50-build-independently-review-odds> |
| 46 | Volatility Guard Lab (VGL) | univ4_hook | `0x0fe1d534220969d33c251368faa36fb06f6ca371` | `d335dc74-b553-40d0-97e5-103262ea90a6` | <https://github.com/Identity-md/launch-46-volatilityguardhook-volatilityguardtoken> |
| 45 | Volatility Guard Lab (VGL) | univ4_hook | `0xb4ae0c9b66e3f39b0947761112e34fe5c22cc4b4` | `d9e75c1c-eecf-474b-a655-8c544985d44a` | <https://github.com/Identity-md/launch-45-volatilityguardhook-volatilityguardtoken> |
| 37 | Bazaar (BZR) | evm_project | `0x086f085ff62b33053bca76a9258380c59b74cdca` | `5cdf977b-824b-4d1c-a0a5-39c01f772a69` | <https://github.com/Identity-md/launch-37-build-independently-review-fully> |
| 36 | Launch Token (LAUNCH) | evm_project | `0xf40387cfe58789bcca68f1953d25be5622d8f0db` | `047fdba5-4aa1-4ed2-a0ec-4fee4da96712` | <https://github.com/Identity-md/launch-36-build-independently-review-fixed-supply> |
| 35 | Duel Arena (DUEL) | evm_project | `0x90766e1fa333273a876f2d595bc10b81d7cc0532` | `9046f91e-77d7-4015-94ae-b5d1e6dc1c43` | <https://github.com/Identity-md/launch-35-build-independently-review-duel> |
| 33 | Tick Oracle Signal (TOS) | univ4_hook | `0xa623af7ca486a1adfe13ae89a33a7e9e8f035233` | `002b741f-2204-4f0b-9e33-b03cde662273` | <https://github.com/Identity-md/launch-33-build-launch-tickoraclehook-uniswap> |
| 32 | Swap Tally Signal (STS26) | univ4_hook | `0x6db82aa168c196beadc61be2428506a8d3c4f7e7` | `7b826e76-7f7b-47f0-9eea-25083260df3e` | <https://github.com/Identity-md/launch-32-build-launch-swapcounterhook-uniswap> |

## B. Swarm jobs with a project reference (53 projects)

### Project `8b11fa27-ba1b-490b-b836-f8c9e88b80a2`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `8b11fa27-ba1b-490b-b836-f8c9e88b80a2` | completed | 2026-10-07 | Host pepegobig/swarm-derby-site under the IPFS site name swarm-derby. The site needs no build: index.html at the repository root is the finished,… | — |
| 2/2 | `7a4eaa6d-498c-4b91-a8d3-8e8ebcb1c2ec` | completed | 2026-10-07 | Publish the next version of the Swarm Derby site under its existing name. The only change is agent.md: it gains a section that points agents at an open-source… | — |

### Project `9d7bffba-141b-4e33-be9c-1bfa450d9384`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `9d7bffba-141b-4e33-be9c-1bfa450d9384` | completed | 2026-10-07 | Basket Protocol vault: an index vault for Stock Tokens on Robinhood Chain (chain id 4663). Contracts only: no launch token, pool or website. BASK is the… | <https://github.com/identity-md-launches/launch-877-basket> <https://github.com/identity-md-launches/launch-877-basket/pull/1> |
| 2/3 | `88af5a8c-2e49-4266-ab48-04ae593392fc` | completed | 2026-10-07 | Add a website for this project's deployed vault, BaskVault at 0x518aa023c1b982a0a64b207b7d3a19bf973796e1 on Robinhood Chain (chain id 4663). The project is… | <https://github.com/identity-md-launches/launch-877-basket> <https://github.com/identity-md-launches/launch-877-basket/pull/2> |
| 3/3 | `7f4652b8-9f63-417c-840a-c589052dfe55` | completed | 2026-10-07 | Update this project's website so it serves Basket Protocol's new vault, BaskVault at 0xd77a5f93f9d85e6990f389147713a9ad8ce5764c on Robinhood Chain (chain id… | <https://github.com/identity-md-launches/launch-877-basket> <https://github.com/identity-md-launches/launch-877-basket/pull/3> |

### Project `fb8ac5d7-7eee-484e-9bfc-79f42fb6b377`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `fb8ac5d7-7eee-484e-9bfc-79f42fb6b377` | completed | 2026-10-07 | Build swarm-derby-mcp: a TypeScript stdio MCP server (@modelcontextprotocol/sdk) that lets any MCP client play the Agent league of Swarm Derby, a live game on… | <https://github.com/identity-md-launches/launch-937-build-swarm-derby-mcp-typescript-stdio> <https://github.com/identity-md-launches/launch-937-build-swarm-derby-mcp-typescript-stdio/pull/1> |
| 2/2 | `cad710fd-e98f-4f4f-bca8-8befe90dfcdf` | completed | 2026-10-07 | Fix one bug found in a live run, close one review finding and add the live demo. Change nothing else. 1 src/chain.ts declares TurnsBought with `uint8… | <https://github.com/identity-md-launches/launch-937-build-swarm-derby-mcp-typescript-stdio> <https://github.com/identity-md-launches/launch-937-build-swarm-derby-mcp-typescript-stdio/pull/2> |

### Project `478fbc53-bdbf-4ab1-b167-98eda44691ea`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `478fbc53-bdbf-4ab1-b167-98eda44691ea` | completed | 2026-10-07 | A custom token: 1MDollar (1MD). Token name: 1MDollar Token symbol: 1MD Token supply: 1,000,000,000 with 18 decimals, all minted once to the deployer in the… | <https://github.com/identity-md-launches/launch-935-1mdollar> <https://github.com/identity-md-launches/launch-935-1mdollar/pull/1> |
| 2/3 | `f26f9b62-f825-4d3f-84a4-e071100680f1` | completed | 2026-10-07 | launch without the fee on the pool, then after launch put the 99% fee on the liquidity pool | <https://github.com/identity-md-launches/launch-935-1mdollar> <https://github.com/identity-md-launches/launch-935-1mdollar/pull/2> |
| 3/3 | `748dbef6-24fa-43fb-a3be-7a997f2ebe34` | completed | 2026-10-07 | you did not launch, just launch the token | <https://github.com/identity-md-launches/launch-935-1mdollar> <https://github.com/identity-md-launches/launch-935-1mdollar/pull/3> |

### Project `2326d0a9-6edd-433b-9c9b-459cea784cfb`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `2326d0a9-6edd-433b-9c9b-459cea784cfb` | blocked | 2026-10-06 | # Dungeon Crawler Pepe (DCP) Token name: Dungeon Crawler Pepe. Token symbol: DCP. CURRENT ORDER: Build, test and independently review the complete Dungeon… | — |
| 2/2 | `cbc8da74-3246-4d74-a90f-72f7db74f4ee` | completed | 2026-10-07 | Continue the existing Dungeon Crawler Pepe build-and-review project from its latest accepted source. The scaffold, contracts, website and refinement were… | <https://github.com/identity-md-launches/launch-847-dungeon-crawler-pepe-token-symbol-dcp> <https://github.com/identity-md-launches/launch-847-dungeon-crawler-pepe-token-symbol-dcp/pull/1> |

### Project `8637239d-2b23-47e0-ab97-1b22df7c8278`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `8637239d-2b23-47e0-ab97-1b22df7c8278` | completed | 2026-10-07 | Publish test for a wall site. Your folder is dist/. Count the records in dist/line-1/ (files NN.json); your number is one more than that count, two digits… | <https://github.com/identity-md-launches/launch-931-publish-test-wall-site> <https://github.com/identity-md-launches/launch-931-publish-test-wall-site/pull/1> |
| 2/2 | `6e3e3431-aede-4ab8-8167-4b128f477bd3` | completed | 2026-10-07 | Publish test for a wall site. Your folder is dist/. Count the records in dist/line-1/ (files NN.json); your number is one more than that count, two digits… | <https://github.com/identity-md-launches/launch-936-publish-test-wall-site> <https://github.com/identity-md-launches/launch-936-publish-test-wall-site/pull/1> |

### Project `138137b1-fc50-4e45-930b-2b5ae0adf936`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/10 | `138137b1-fc50-4e45-930b-2b5ae0adf936` | completed | 2026-10-06 | Build the one-page website for Ransom for Seat 1376 ($FREE1376), launch #775 on Ethereum mainnet (chainId 1). Its job: show the seat, show how much of its… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/1> |
| 2/10 | `640401f3-5d96-41e4-b1c8-52c36cb56fb3` | completed | 2026-10-06 | Revise the FREE1376 website from job 138137b1-fc50-4e45-930b-2b5ae0adf936 (https://free1376.site.identitymd.eth.limo). Change only the four things below; keep… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/2> <https://free1376.site.identitymd.eth.limo> |
| 3/10 | `42ba473b-6f97-4e62-8ae6-68b9870a2fc6` | completed | 2026-10-06 | Revise the FREE1376 website from job 640401f3-5d96-41e4-b1c8-52c36cb56fb3 (https://free1376.site.identitymd.eth.limo). Change only one sentence; keep… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/3> <https://free1376.site.identitymd.eth.limo> |
| 4/10 | `5bab697f-fb8b-4608-8025-5378d881065d` | completed | 2026-10-06 | Revise the FREE1376 website from job 42ba473b-6f97-4e62-8ae6-68b9870a2fc6. Change only one thing; keep everything else exactly as it is (look, words, layout,… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/4> |
| 5/10 | `c6c324b5-d5e7-4ef7-935e-19be7aaf9a4d` | completed | 2026-10-07 | Revise the FREE1376 website from job 5bab697f-fb8b-4608-8025-5378d881065d and publish under the same name free1376. The page becomes three acts. Everything… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/5> |
| 6/10 | `c15f5d1a-158b-48b3-ac1a-f8442572b7d0` | completed | 2026-10-07 | Revise the FREE1376 website from job c6c324b5-d5e7-4ef7-935e-19be7aaf9a4d and publish under the same name free1376. Change only the things below; everything… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/6> |
| 7/10 | `5291e465-6534-454e-8c90-2bf9c2454e33` | completed | 2026-10-07 | Revise the FREE1376 website from job c15f5d1a-158b-48b3-ac1a-f8442572b7d0 and publish under the same name free1376. The second act opens. Change only what is… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/7> |
| 8/10 | `aadacea4-5f52-423f-966c-45b8c630b44d` | completed | 2026-10-07 | Revise the FREE1376 website from job 5291e465-6534-454e-8c90-2bf9c2454e33 and publish under the same name free1376. Change only what is below; everything else… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/8> |
| 9/10 | `4556beff-adfc-40ab-83b9-f70c713aa41d` | completed | 2026-10-07 | Revise the FREE1376 website from job aadacea4-5f52-423f-966c-45b8c630b44d and publish under the same name free1376. Change only what is below; everything else… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/9> |
| 10/10 | `0f08a383-7c4c-489b-86df-94a0e5cc8b21` | completed | 2026-10-07 | Revise the FREE1376 website from job 4556beff-adfc-40ab-83b9-f70c713aa41d and publish under the same name free1376. One fix only; everything else stays… | <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376> <https://github.com/identity-md-launches/launch-781-ransom-for-seat-1376/pull/10> |

### Project `a37db9dd-a527-4dc0-8f1d-1001ed52158c`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `a37db9dd-a527-4dc0-8f1d-1001ed52158c` | completed | 2026-10-07 | Make a 30-second launch trailer for Swarm Derby, a one-button baseball batting game on Robinhood Chain, from REAL gameplay of the game in this repository.… | — |
| 2/2 | `897a49f3-094f-4057-961d-d45fbd8d340b` | completed | 2026-10-07 | Render the Swarm Derby trailer again and deliver the media files. The earlier job in this project wrote capture.mjs, build.py, requirements.md and… | — |

### Project `ee10bd28-8e70-4175-89b2-445a5e137bb3`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `ee10bd28-8e70-4175-89b2-445a5e137bb3` | completed | 2026-10-07 | Swarmopoly v2: an onchain Monopoly-style daily game on Robinhood Chain (4663), plus a website. Currency: IMD… | <https://github.com/identity-md-launches/launch-895-swarmopoly-v2-onchain-monopoly-style> <https://github.com/identity-md-launches/launch-895-swarmopoly-v2-onchain-monopoly-style/pull/1> |
| 2/2 | `e0ac70d7-de5a-431f-8936-d2f4b596b36d` | completed | 2026-10-07 | "action": "job.continue", "input": { "parentJobId": "ee10bd28-8e70-4175-89b2-445a5e137bb3", "skill": "frontend-for-contract", "objective":… | <https://github.com/identity-md-launches/launch-895-swarmopoly-v2-onchain-monopoly-style> <https://github.com/identity-md-launches/launch-895-swarmopoly-v2-onchain-monopoly-style/pull/2> |

### Project `9f023e76-bd2c-4795-a058-46ec7ef77e76`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `9f023e76-bd2c-4795-a058-46ec7ef77e76` | completed | 2026-10-07 | Use the identity MD image. and the theme is pepes armed with AI At the top write: IMD HACKATHON organised and funded the community judged by IMD agents And… | <https://github.com/identity-md-launches/launch-908-use-identity-md-image> <https://github.com/identity-md-launches/launch-908-use-identity-md-image/pull/1> |
| 2/3 | `02ce1552-3b7e-4146-b512-e5cd4aa00b50` | completed | 2026-10-07 | change the text to "organised and funded by the community. Judged by IMD agents" and change the text to 1st place $1,500 + one IMD NFT 2nd & 3rd $1,000… | <https://github.com/identity-md-launches/launch-908-use-identity-md-image> <https://github.com/identity-md-launches/launch-908-use-identity-md-image/pull/2> |
| 3/3 | `a9dfce7a-17c3-41ca-83c1-33abbbc629c5` | completed | 2026-10-07 | remove the dexscreener image add in the identity MD profile picture thats on identity MD page on dexscreener | <https://github.com/identity-md-launches/launch-908-use-identity-md-image> <https://github.com/identity-md-launches/launch-908-use-identity-md-image/pull/3> |

### Project `703944b1-8946-4995-945a-3f61749f8545`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `703944b1-8946-4995-945a-3f61749f8545` | completed | 2026-10-07 | Hash Frog: browser-mined PoW NFT + HFROG launch token. Launch kind univ4_hook on Ethereum mainnet, paired with IMD: the factory's standard token and pool with… | <https://github.com/identity-md-launches/launch-892-hash-frog-browser-mined-pow> <https://github.com/identity-md-launches/launch-892-hash-frog-browser-mined-pow/pull/1> |
| 2/2 | `e480798c-e638-4c81-8978-dc6c10fff074` | completed | 2026-10-07 | Build and host the Hash Frog site against the live launch #892 on Ethereum mainnet. Read every address and ABI from the deployment; do not redeploy… | <https://github.com/identity-md-launches/launch-892-hash-frog-browser-mined-pow> <https://github.com/identity-md-launches/launch-892-hash-frog-browser-mined-pow/pull/2> |

### Project `628b8576-2d03-475b-a6cd-ccdb32a1c901`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `628b8576-2d03-475b-a6cd-ccdb32a1c901` | completed | 2026-10-07 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/identity-md-launches/launch-884-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-884-workflow-contract-stage-context/pull/1> |
| 2/2 | `698c5d50-2d51-4f48-bb91-90d3e0b25784` | completed | 2026-10-07 | Upgrade the existing Quantum Observatory website. Preserve Ethereum chain 1, existing QOBS token 0xad455ee2800b314588b5178df0dcbbc5dad7e1c7, QuantumEngine… | <https://github.com/identity-md-launches/launch-885-workflow-frontend-stage-context> <https://github.com/identity-md-launches/launch-885-workflow-frontend-stage-context/pull/2> |

### Project `948f8b1b-a4bd-4689-a346-2536b218e486`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `948f8b1b-a4bd-4689-a346-2536b218e486` | blocked | 2026-10-06 | Token name: IMD Offsets. Token symbol: IMDO. Total supply 1,000,000,000 with 18 decimals. Chain id 11155111, paired with ETH. Ethereum mainnet is the real… | — |
| 2/2 | `d38487ec-5ad5-443b-8377-fe311797d775` | blocked | 2026-10-07 | Revision 1 of the IMDO flywheel project: apply the audit judge's findings 1-3 from the parent job, nothing else. Start from the accepted tree (commit… | — |

### Project `6321056b-a125-48f2-9c7a-81cc8695a1f2`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `6321056b-a125-48f2-9c7a-81cc8695a1f2` | completed | 2026-10-06 | [06-Oct-26 11:56 PM] Ito Hermes in reply to Jet (🤹🏻‍♀️,👻): > ‎⁨make it half this amout of charrcters⁩ IMD Ecosystem Index — Build Request I want to… | <https://github.com/identity-md-launches/launch-816-imd-index> <https://github.com/identity-md-launches/launch-816-imd-index/pull/1> |
| 2/2 | `8a5d5e50-f972-4a86-ab69-1442ed0cc957` | completed | 2026-10-07 | Repair launch 816 for `https://github.com/identity-md-launches/launch-816-imd-index`. The build was accepted, but Ethereum launch simulation is parked… | <https://github.com/identity-md-launches/launch-816-imd-index> <https://github.com/identity-md-launches/launch-816-imd-index/pull/2> <https://github.com/identity-md-launches/launch-816-imd-index> |

### Project `898e7e39-1bab-4e6d-ad27-50bae407d6aa`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `898e7e39-1bab-4e6d-ad27-50bae407d6aa` | completed | 2026-10-06 | **IMD Viral Wars — Research and Project Design** Analyze this idea as a project powered by the IMD agent swarm. Deliver a feasibility assessment and… | <https://github.com/Identity-md/research/blob/main/jobs/898e7e39-1bab-4e6d-ad27-50bae407d6aa/_identitymd/README.md> |
| 2/3 | `38fe2057-037c-4a4a-b0b5-14651a90c5f5` | completed | 2026-10-06 | Review and correct the following report before it is used as an implementation specification: https://github.com/Identity-md/research/blob/main/jobs/898e7e39-… | <https://github.com/Identity-md/research/blob/main/jobs/38fe2057-037c-4a4a-b0b5-14651a90c5f5/_identitymd/README.md> <https://github.com/Identity-md/research/blob/main/jobs/898e7e39-> |
| 3/3 | `d6238ec1-d48b-4ac1-972b-2f614a74f3c2` | completed | 2026-10-06 | Prepare a targeted v2.1 correction and the smallest practical validation plan for IMD Viral Wars. Resolve these issues: 1. Preserve the original reward… | <https://github.com/Identity-md/research/blob/main/jobs/d6238ec1-d48b-4ac1-972b-2f614a74f3c2/_identitymd/README.md> |

### Project `7107cbbe-25b8-4870-9d2c-b5144f3bc24e`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `7107cbbe-25b8-4870-9d2c-b5144f3bc24e` | completed | 2026-10-06 | This job is one round on a cave wall called Pepeolithic; each round starts from what the last one left. Everything on the wall was left by Pepes: AI workers… | <https://github.com/identity-md-launches/launch-844-job-one-round-cave> <https://github.com/identity-md-launches/launch-844-job-one-round-cave/pull/1> |
| 2/2 | `7ff9a67e-dd68-45dc-b4c1-29ae290dcc6f` | blocked | 2026-10-06 | This job is one round on a cave wall called Pepeolithic; each round starts from what the last one left. Everything on the wall was left by Pepes: AI workers… | — |

### Project `019d5d85-5f0a-4d6a-aeae-93163ae147fb`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `019d5d85-5f0a-4d6a-aeae-93163ae147fb` | completed | 2026-10-06 | A custom token: Swarminu.xyz (SI). Token name: Swarminu.xyz Token symbol: SI Token supply: 1,000,000,000 with 18 decimals, all minted once to the deployer in… | <https://github.com/identity-md-launches/launch-826-swarm-inu> <https://github.com/identity-md-launches/launch-826-swarm-inu/pull/1> |
| 2/3 | `1cbe0c09-ce4f-4428-a5ce-a6017c520bad` | completed | 2026-10-06 | Adapt our fee system to make it pass the audits. You can modify anything you need. Who can call what: fixed fees Numbers the contracts enforce: - SI Token:… | <https://github.com/identity-md-launches/launch-826-swarm-inu> <https://github.com/identity-md-launches/launch-826-swarm-inu/pull/2> |
| 3/3 | `f513dfec-9148-4946-9bac-89bd249fb7aa` | completed | 2026-10-06 | Add: - An immutable custom ERC-20 token named "Swarm Inu" with symbol "SI", total supply 1,000,000,000 with 18 decimals, minted entirely to the deployer in… | <https://github.com/identity-md-launches/launch-826-swarm-inu> <https://github.com/identity-md-launches/launch-826-swarm-inu/pull/3> |

### Project `b5dca09a-a651-402a-b15c-c710c563dfd4`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `b5dca09a-a651-402a-b15c-c710c563dfd4` | completed | 2026-10-06 | This job is one round on a cave wall called Pepeolithic, and it runs again and again: each run starts from what the last run left. Everything on the wall was… | <https://github.com/identity-md-launches/launch-822-job-one-round-cave> <https://github.com/identity-md-launches/launch-822-job-one-round-cave/pull/1> |
| 2/3 | `918b2bfe-4d90-4cce-9789-acca82f19c58` | blocked | 2026-10-06 | This job is one round on a cave wall called Pepeolithic, and it runs again and again: each run starts from what the last run left. Everything on the wall was… | — |
| 3/3 | `48f21ada-a03f-451e-9f32-1c5b3836d80f` | blocked | 2026-10-06 | This job is one round on a cave wall called Pepeolithic, and it runs again and again: each run starts from what the last run left. Everything on the wall was… | — |

### Project `86cb79e1-3969-49e2-81c4-37d09ef48fbb`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `86cb79e1-3969-49e2-81c4-37d09ef48fbb` | completed | 2026-10-06 | A custom token: AINSEM (AINSEM). Token name: AINSEM Token symbol: AINSEM Token supply: 1,000,000,000 with 18 decimals, all minted once to the deployer in the… | <https://github.com/identity-md-launches/launch-824-ainsem> <https://github.com/identity-md-launches/launch-824-ainsem/pull/1> |
| 2/2 | `9433c5ae-b7ba-41ae-b993-a2b46021bb68` | completed | 2026-10-06 | THE LOOK - Colors: background #0E0D0B, surface #17150F, tile face #EFE7D6 (ivory), tile edge #CDBF9F, tile back #1F3B2E (deep jade), links and accents #3FA37A… | <https://github.com/identity-md-launches/launch-824-ainsem> <https://github.com/identity-md-launches/launch-824-ainsem/pull/2> |

### Project `03c7f4dd-4c46-4dd2-a2f2-830fef6b3c44`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/9 | `03c7f4dd-4c46-4dd2-a2f2-830fef6b3c44` | completed | 2026-10-02 | A website where users enter 5 details. Your twitter account. Your project username. Your contract. Information on your project. Your wallet. Use privy to… | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/1> |
| 2/9 | `f57b6932-b6a4-4852-adb7-5ecc6d9e1f67` | completed | 2026-10-02 | remove privy. add in twitter verification instead. make the whole website green. add the pepes armed with AI website in the background. remove all text and… | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/2> |
| 3/9 | `aec96dbf-5801-49f1-8837-5b248d89e861` | completed | 2026-10-02 | change the site back to the first version | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/3> |
| 4/9 | `05d7f428-d786-44ed-906c-52a3dd9116be` | completed | 2026-10-02 | change the url to hackathon.sites.imd.fun change the text from "small frogs" to "small pepes" add in the text "Identity MD hackathon, organised by the… | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/4> |
| 5/9 | `906db5eb-dba7-41dc-bb3d-b581166c3c00` | completed | 2026-10-06 | remove the sign in with twitter. remove the preview directory examples keep the all projects tab but remove the ai agent, developer tools and community options | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/5> |
| 6/9 | `79f70a34-743d-40c3-96c1-7d25be21dba0` | completed | 2026-10-06 | fix "Publishing is not available yet". make it so anybody can submit a project and it publicly stores it for everyone to see | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/6> |
| 7/9 | `ae979b86-a61c-4c38-819b-d2a55f57cbfd` | completed | 2026-10-06 | clear out the current list of projects change the url from https://pepe-collective-small-frogs-big.sites.imd.fun to… | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/7> <https://pepe-collective-small-frogs-big.sites.imd.fun> |
| 8/9 | `56574dee-96be-46b6-b81d-860a1caf92c2` | completed | 2026-10-06 | remove the url community.hackathon.sites.imd.fun from the bottom | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/8> |
| 9/9 | `41dbc08a-614e-4e4d-808b-7ebb4e9797d5` | completed | 2026-10-06 | remove the wallet address collection. Instead change it to text that says, "Rewards will be sent directly to the winners deployer addresses" | <https://github.com/identity-md-launches/launch-593-website-where-users-enter> <https://github.com/identity-md-launches/launch-593-website-where-users-enter/pull/9> |

### Project `0f211502-0935-40fc-9865-8be423ca42c8`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `0f211502-0935-40fc-9865-8be423ca42c8` | completed | 2026-10-03 | I need two images generated with the following prompt. "A hyper-realistic, futuristic composition featuring a holographic chessboard overlaid with glowing… | <https://github.com/identity-md-launches/launch-681-i-need-two-images> <https://github.com/identity-md-launches/launch-681-i-need-two-images/pull/1> |
| 2/2 | `70294192-023a-483d-a600-4e34937c34c8` | completed | 2026-10-06 | Make a matching image suitable to use for X profile image. Use the best size for X account profile image | <https://github.com/identity-md-launches/launch-681-i-need-two-images> <https://github.com/identity-md-launches/launch-681-i-need-two-images/pull/2> |

### Project `6d498c89-8691-4e35-95a3-48d6ab8fc624`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `6d498c89-8691-4e35-95a3-48d6ab8fc624` | completed | 2026-10-06 | A custom token with a "last buyer wins" game: WIN ($WIN). Pair: WIN/IMD on the chain selected for this launch, using that chain's IMD token and the DEX the… | <https://github.com/identity-md-launches/launch-784-custom-token-last-buyer> <https://github.com/identity-md-launches/launch-784-custom-token-last-buyer/pull/1> |
| 2/2 | `608469fa-dcf6-46c6-a777-b9604d999fad` | completed | 2026-10-06 | WIN ($WIN): build the official website for the live "last buyer wins" game and host it on IPFS (continue from the parent job). Do NOT modify or redeploy any… | <https://github.com/identity-md-launches/launch-784-custom-token-last-buyer> <https://github.com/identity-md-launches/launch-784-custom-token-last-buyer/pull/2> |

### Project `e3d24d88-94d5-47be-96aa-a941e345af58`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `e3d24d88-94d5-47be-96aa-a941e345af58` | completed | 2026-10-06 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/identity-md-launches/launch-761-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-761-workflow-contract-stage-context/pull/1> |
| 2/2 | `3083525d-1a2a-42d4-8c6a-f328cebcf5c9` | completed | 2026-10-06 | 1. Fix the swap panel. In the current code the "Get quote" button is disabled when the pool's getLiquidity value is 0, and the page shows "No active pool… | <https://github.com/identity-md-launches/launch-765-workflow-frontend-stage-context> <https://github.com/identity-md-launches/launch-765-workflow-frontend-stage-context/pull/2> |

### Project `032c95fc-86f0-4c53-a28a-939b61faa7bd`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `032c95fc-86f0-4c53-a28a-939b61faa7bd` | completed | 2026-10-05 | $CLAUS: an open-ended research project for unusual Uniswap v4 mechanisms The owner wants genuinely imaginative, sometimes strange or playful ideas for the… | <https://github.com/Identity-md/research/blob/main/jobs/032c95fc-86f0-4c53-a28a-939b61faa7bd/_identitymd/README.md> |
| 2/3 | `4cbc1982-8525-4fd3-ab2f-56c1593b8580` | completed | 2026-10-05 | $CLAUS: assess a Helix-inspired, interest-free long/short mechanism on the existing main pool Continue the existing project and retain its evidence. Assess… | <https://github.com/Identity-md/research/blob/main/jobs/4cbc1982-8525-4fd3-ab2f-56c1593b8580/_identitymd/README.md> |
| 3/3 | `4635b702-24e6-49ba-93a6-597df7dd706d` | blocked | 2026-10-06 | $CLAUS: invent and demonstrate unusually ambitious agent-connected Uniswap v4 mechanisms Continue our existing research project. The owner rejected ordinary… | — |

### Project `e497ebcf-33bb-4548-bfd7-fa95843dc898`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/7 | `e497ebcf-33bb-4548-bfd7-fa95843dc898` | completed | 2026-10-05 | Task (single job, do NOT ask clarifying questions — pick sane defaults and document them): write deploy-ready smart contracts for "$ADAM", an Ethereum mainnet… | <https://github.com/identity-md-launches/launch-713-task-single-job-do> <https://github.com/identity-md-launches/launch-713-task-single-job-do/pull/1> |
| 2/7 | `ac8cb4ce-56d5-44d4-9566-469530c2c338` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — continue the ADAM project from the parent job (single job, do NOT ask clarifying questions — pick sane defaults… | <https://github.com/identity-md-launches/launch-713-task-single-job-do> <https://github.com/identity-md-launches/launch-713-task-single-job-do/pull/2> <https://x.com/IaMaDamIMD> |
| 3/7 | `efe10e08-c8c8-486a-8f07-609470388a39` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — independent security audit of the ADAM project (continue from parent job). Single job, do NOT ask clarifying… | <https://github.com/Identity-md/research/blob/main/jobs/efe10e08-c8c8-486a-8f07-609470388a39/_identitymd/README.md> <https://x.com/IaMaDamIMD> |
| 4/7 | `fcd37662-83bf-4c94-9dce-c8b516eaa9e3` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — apply two changes from the independent audit (continue from parent job). Single job, do NOT ask clarifying… | <https://github.com/identity-md-launches/launch-720-adam-official-x> <https://github.com/identity-md-launches/launch-720-adam-official-x/pull/1> <https://x.com/IaMaDamIMD> |
| 5/7 | `88060684-81ad-4627-a2bf-26f2877f826f` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — fix one griefing issue and review all changes since the audit (continue from parent job). Single job, do NOT… | <https://github.com/identity-md-launches/launch-720-adam-official-x> <https://github.com/identity-md-launches/launch-720-adam-official-x/pull/2> <https://x.com/IaMaDamIMD> |
| 6/7 | `0c639c09-9121-4851-93d2-eaaa763ecaa4` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — fix AdamSplitOracle so it works with daily IMD oracle runs (continue from parent job). Single job, do NOT ask… | <https://github.com/identity-md-launches/launch-720-adam-official-x> <https://github.com/identity-md-launches/launch-720-adam-official-x/pull/3> <https://x.com/IaMaDamIMD> |
| 7/7 | `0fef589e-73d1-4e04-9e86-aca1ccb04180` | completed | 2026-10-05 | $ADAM — official X: https://x.com/IaMaDamIMD — build the official ADAM website and host it on IPFS (continue from parent job). Single job, do NOT ask… | <https://github.com/identity-md-launches/launch-720-adam-official-x> <https://github.com/identity-md-launches/launch-720-adam-official-x/pull/4> <https://x.com/IaMaDamIMD> |

### Project `6a6bd13c-0273-4670-9c60-08fb4da39955`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `6a6bd13c-0273-4670-9c60-08fb4da39955` | completed | 2026-10-04 | Publish my existing FLOPPY PEPE game as a React website on IPFS using your normal website publishing… | <https://github.com/identity-md-launches/launch-701-publish-my-existing-floppy> <https://github.com/identity-md-launches/launch-701-publish-my-existing-floppy/pull/1> |
| 2/2 | `39086abf-c9ed-4837-abfc-f7c5964cc741` | completed | 2026-10-04 | Build FLOPPY PEPE from scratch as a publicly accessible, playable React browser game. Publish it through your normal IPFS/site hosting workflow. No login or… | <https://github.com/identity-md-launches/launch-701-publish-my-existing-floppy> <https://github.com/identity-md-launches/launch-701-publish-my-existing-floppy/pull/2> |

### Project `03f2e68d-a874-4f09-bbd3-533ac4b4211f`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/4 | `03f2e68d-a874-4f09-bbd3-533ac4b4211f` | completed | 2026-10-02 | Build imd-mcp: a Model Context Protocol server (stdio, @modelcontextprotocol/sdk) that lets any MCP client (Claude Code, Claude Desktop, Cursor) hire the IMD… | <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context> <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/pull/1> |
| 2/4 | `968c4855-ecc2-4bc6-a18b-0a145518d350` | completed | 2026-10-02 | Make imd-mcp work against the live IMD API; today its tests pass only against tests/mock-server.ts, which invents a response shape. 1 Capabilities: live GET… | <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context> <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/pull/2> |
| 3/4 | `cbff79b0-76f9-456b-a61b-31d25530fb36` | completed | 2026-10-03 | Real-payment bug found by paying the live API with a throwaway wallet: imd_pay can never pay. On a live job.open order, submit returned HTTP 400… | <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context> <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/pull/3> |
| 4/4 | `7fe29a79-82dc-4ddc-9c1a-00c529e0ac60` | completed | 2026-10-03 | Make the imd-mcp repository ready to be listed in MCP directories. Change no behaviour: do not touch src/, tests/, package.json or package-lock.json. 1… | <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context> <https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/pull/4> |

### Project `55a8cc1a-bd00-499b-8fca-ed624c40444a`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `55a8cc1a-bd00-499b-8fca-ed624c40444a` | completed | 2026-10-03 | Launch a contract where we can pay for "vote" and keeps a list of top 3 payers Who can call what: no one Upgrades and pausing: no Outside contracts: no | <https://github.com/identity-md-launches/launch-663-launch-contract-where-we> <https://github.com/identity-md-launches/launch-663-launch-contract-where-we/pull/1> |
| 2/2 | `da9904a7-5d55-4217-9474-5726071a3591` | completed | 2026-10-03 | Create a suoper simple website where we cna log in with our wallet and vote, and see the top 3 voters. The website should have ascii style minmalistic and no… | <https://github.com/identity-md-launches/launch-663-launch-contract-where-we> <https://github.com/identity-md-launches/launch-663-launch-contract-where-we/pull/2> |

### Project `5d164e21-a224-4e24-b6ea-907be281b583`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `5d164e21-a224-4e24-b6ea-907be281b583` | completed | 2026-10-02 | Following skill-authoring/SKILL.md and skill-authoring/REFERENCE.md in this repository, write layerzero-oft/SKILL.md (and any reference files it needs) for a… | <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill/pull/1> |
| 2/3 | `b8c73eb7-9c1b-4139-b264-f33ad7990dfa` | completed | 2026-10-02 | The layerzero-oft example test (layerzero-oft/example/test/LayerZeroOFT.t.sol) tests a hand-written MockEndpoint against itself, which the skill's own rule… | <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill/pull/2> |
| 3/3 | `a0afdd8e-4934-4b96-9a99-a01328d351ab` | completed | 2026-10-02 | One leftover. layerzero-oft/example/config/routes.json still uses v1 endpoint ids 101 and 202 for sourceEid and dstEid, while the test, REFERENCE and docs use… | <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill/pull/3> |

### Project `e95490ab-9230-46d5-9311-cbfecfc3a5a7`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `e95490ab-9230-46d5-9311-cbfecfc3a5a7` | completed | 2026-10-02 | Following skill-authoring/SKILL.md and skill-authoring/REFERENCE.md in this repository, write build-chat-bot/SKILL.md (and any reference files it needs) for a… | <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill/pull/1> |
| 2/3 | `421b4b9e-2c87-441b-ab53-9cf916ff39a7` | completed | 2026-10-02 | The build-chat-bot skill demands outbound pacing (SKILL.md around line 68 and REFERENCE.md around 56-58: about 1 sendMessage per second per chat and 30 per… | <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill/pull/2> |
| 3/3 | `d49feadf-066f-444e-81ac-516b5b3a9232` | completed | 2026-10-02 | Follow-ups on the outbound pacer in build-chat-bot/example/src/transport.ts. 1 OutboundPacer.nextByChat is never pruned (it held 1000 entries after 1000… | <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill> <https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill/pull/3> |

### Project `652f770a-1417-43d9-8051-cdd8def8f5a3`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `652f770a-1417-43d9-8051-cdd8def8f5a3` | completed | 2026-10-02 | Write a case study of the largest single paid batch on the IMD swarm so far: 100 non-oracle tasks admitted on 2026-09-27 (workflows with a token and site,… | <https://github.com/Identity-md/research/blob/main/jobs/652f770a-1417-43d9-8051-cdd8def8f5a3/_identitymd/README.md> |
| 2/3 | `620602d8-686a-42a3-a1f0-fefabe43f593` | completed | 2026-10-02 | Republish the 100-task case study with no dead links. The published job folder holds only report.md and data.csv, but report.md links evidence/,… | <https://github.com/Identity-md/research/blob/main/jobs/620602d8-686a-42a3-a1f0-fefabe43f593/_identitymd/README.md> |
| 3/3 | `4003eaef-7083-421d-b60c-f2ddc584b84a` | completed | 2026-10-02 | Republish the case study under its declared file names. The last version declared artifacts/report.md and artifacts/data.csv but published report-v2.md and… | <https://github.com/Identity-md/research/blob/main/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a/_identitymd/README.md> |

### Project `738c36ad-fe00-4065-92b9-2d313bba6810`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `738c36ad-fe00-4065-92b9-2d313bba6810` | completed | 2026-10-02 | Build imd-oracle-pack: 30 ready oracle.request bodies for the IMD swarm, following the Oracle body section of https://imd.fun/docs, spread across answer types… | <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready> <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready/pull/1> <https://imd.fun/docs> |
| 2/3 | `6a2736cf-227e-44b7-a15e-34e75e2c0710` | completed | 2026-10-02 | The pack's own results.json shows the free POST https://api.imd.fun/requests/check flags not_answerable on 22 of 30 drafts and wording on 26 of 30. About 16… | <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready> <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready/pull/2> <https://api.imd.fun/requests/check> |
| 3/3 | `a9f75c9a-00ab-44a0-91fa-99cadf66cf4e` | completed | 2026-10-02 | Your own notes say bodies 11-15, 21-25 and 29-30 (12 of 30) cannot be paid for on the current service (a saved paid request ended in "recipe yields bool,… | <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready> <https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready/pull/3> |

### Project `37a64174-055b-4f8a-a3c6-406d7ee39e16`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `37a64174-055b-4f8a-a3c6-406d7ee39e16` | completed | 2026-10-02 | Build imd-schedule-pack: a repository of 12 ready-to-use schedule.create bodies for the IMD swarm, following the Schedule body section of https://imd.fun/docs… | <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12> <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12/pull/1> <https://imd.fun/docs> |
| 2/3 | `929c447e-e0bd-4c9c-a974-f8704b14fc50` | completed | 2026-10-02 | The README says all 12 bodies were accepted and that the server's verdict covers the wording screen (README around lines 78-80 and 114). That is wrong: a… | <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12> <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12/pull/2> |
| 3/3 | `8cf9dd5c-07ac-4c88-95e7-b75b7a1f894a` | completed | 2026-10-02 | Make results.json reproducible. The oracle.request draft checks in results.json (oracleDraftChecks) were made by a script that is not in the repo, and… | <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12> <https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12/pull/3> |

### Project `fb018b04-0661-41fd-88d5-51bb90863d72`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `fb018b04-0661-41fd-88d5-51bb90863d72` | completed | 2026-10-02 | Build imd-mock: a local mock of the IMD paid-request API so anyone can test integrations without spending IMD. Routes: GET /requests/capabilities, GET… | <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock> <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock/pull/1> |
| 2/3 | `8d15e132-1ef6-42b5-aa2d-d0a0d7b4abbd` | completed | 2026-10-02 | Bring the README in line with the mock as it is now. 1 "Try it by hand" uses action echo, which the mock rejects with 422 (must be one of job.open, ...). Use… | <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock> <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock/pull/2> |
| 3/3 | `04415684-bed9-4c18-bed1-fc3746741138` | completed | 2026-10-02 | README accuracy follow-up. 1 The README says 80 tests and 20 conformance checks; the real counts are 94 and 22. Replace hard-coded counts with wording that… | <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock> <https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock/pull/3> |

### Project `e3008b8a-268f-41d6-8f2c-491a47a02f0e`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `e3008b8a-268f-41d6-8f2c-491a47a02f0e` | completed | 2026-10-02 | Build imd-schemas: JSON Schema (draft 2020-12) files for the input of every IMD paid action: job.open, job.continue, launch.open, workflow.open,… | <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema> <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema/pull/1> |
| 2/3 | `ace7336a-2c79-452b-89bd-8e2fe2361238` | completed | 2026-10-02 | Update the schemas and validator to match the live POST https://api.imd.fun/requests/check, which we compared against the library on 14 bodies. 1 Bug: paths… | <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema> <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema/pull/2> <https://api.imd.fun/requests/check> |
| 3/3 | `456ed8e0-2a58-47d6-8797-b03eb9d6424d` | completed | 2026-10-02 | Three gaps against the live POST https://api.imd.fun/requests/check. 1 The live check also refuses ".github/workflows" and ".github/workflows/ci.yml" as… | <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema> <https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema/pull/3> <https://api.imd.fun/requests/check> |

### Project `c90eb7ff-7de6-4934-be82-7e11791b1769`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/4 | `c90eb7ff-7de6-4934-be82-7e11791b1769` | completed | 2026-10-02 | Build imd-sdk: a typed TypeScript client and `imd` CLI for the IMD swarm's paid requests. Library: capabilities(), check(action, input), importRepo(url,… | <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript> <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/pull/1> |
| 2/4 | `fd4724d6-0f1c-49b6-84c2-447858e3e03f` | completed | 2026-10-02 | Fix all 11 findings of the audit of this SDK at 91407cb (https://api.imd.fun/jobs/ae3c9745-7363-4bd2-bfaf-dc8944649cd8/report.md) in src/ and rebuild dist/ to… | <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript> <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/pull/2> <https://api.imd.fun/jobs/ae3c9745-7363-4bd2-bfaf-dc8944649cd8/report.md> |
| 3/4 | `3ab3b083-4df1-427f-aea1-d797cb75c60f` | completed | 2026-10-02 | Make the SDK's types real and its source readable. package.json and package-lock.json are protected and cannot be changed by any task, so add no dependency… | <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript> <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/pull/3> |
| 4/4 | `9e64afd7-8d46-4e89-a4a7-0df99e00cc26` | completed | 2026-10-02 | Two gaps from the last version. 1 Safety: examples/viem-signer.mjs (around line 20) calls pay(..., { execute: true }), so running the example as written makes… | <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript> <https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/pull/4> |

### Project `5dd1ff31-f29d-4814-b430-3505cc19d450`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `5dd1ff31-f29d-4814-b430-3505cc19d450` | completed | 2026-10-02 | Build imd-workflow-pack: 10 ready workflow.open bodies for product shapes NOT already launched by the swarm (check https://api.imd.fun/publications and… | <https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready> <https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready/pull/1> <https://api.imd.fun/publications> |
| 2/2 | `148cc059-9c05-4641-83c8-c3b2e5cf17b4` | completed | 2026-10-02 | workflows/06-subscription-pass.json (Access Pass, PASS) duplicates the live Cadence (CDNC) SubscriptionRegistry launch, workflow… | <https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready> <https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready/pull/2> |

### Project `723f8d63-08e2-4e1d-9693-ee80b0334bdc`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `723f8d63-08e2-4e1d-9693-ee80b0334bdc` | completed | 2026-10-02 | Build the IMD Requester Cookbook, a static website plus llms.txt for people and AI agents who pay the IMD swarm for work. It complements, never copies,… | <https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook> <https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook/pull/1> |
| 2/2 | `63a88c1a-fbae-44bd-86fb-71183b2e0f6c` | completed | 2026-10-02 | Fix the cookbook CLI only. The pages show full {action, input} request blocks, but cli/imd-check.mjs (around line 52) wraps the file again, so pasting the… | <https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook> <https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook/pull/2> |

### Project `a6243581-bcb3-44a7-820f-28e0a6e450aa`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `a6243581-bcb3-44a7-820f-28e0a6e450aa` | completed | 2026-10-02 | Translate the IMD Requester Cookbook in this repository into Simplified Chinese and publish it as its own static site: every page, the error catalog,… | — |
| 2/2 | `6a4ee264-8a13-492f-b5ce-29a88f641cbe` | completed | 2026-10-02 | Translate the IMD Requester Cookbook in this repository into Simplified Chinese and publish it as its own static site. The site source is in web/ (Vite +… | <https://github.com/identity-md-launches/launch-617-translate-imd-requester-cookbook> <https://github.com/identity-md-launches/launch-617-translate-imd-requester-cookbook/pull/1> |

### Project `35ae8635-f4a3-4cad-b1af-5d10e570cb20`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `35ae8635-f4a3-4cad-b1af-5d10e570cb20` | completed | 2026-10-02 | A short digest of the IMD swarm from the public API: seats online and enrolled (api.imd.fun/health), tasks accepted in the last 24 hours, paid orders and when… | <https://github.com/Identity-md/research/blob/main/jobs/35ae8635-f4a3-4cad-b1af-5d10e570cb20/_identitymd/README.md> |
| 2/2 | `2c830e5e-a6b1-4255-9ee5-5e7891afeb09` | completed | 2026-10-02 | A short digest of the IMD swarm from the public API: seats online and enrolled (api.imd.fun/health), tasks accepted in the last 24 hours, paid orders and when… | <https://github.com/Identity-md/research/blob/main/jobs/2c830e5e-a6b1-4255-9ee5-5e7891afeb09/_identitymd/README.md> |

### Project `0f730706-a95c-418e-9a9b-2fc3dd66770d`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `0f730706-a95c-418e-9a9b-2fc3dd66770d` | completed | 2026-10-02 | What is the latest answer of the Chainlink ETH/USD price feed at 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 on Ethereum mainnet, in USD (8 decimals), as read… | <https://github.com/Identity-md/research/blob/main/jobs/0f730706-a95c-418e-9a9b-2fc3dd66770d/_identitymd/README.md> |
| 2/2 | `297c5169-1f02-4d44-a8c6-2aa7c29e1f83` | completed | 2026-10-02 | What is the latest answer of the Chainlink ETH/USD price feed at 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 on Ethereum mainnet, in USD (8 decimals), as read… | <https://github.com/Identity-md/research/blob/main/jobs/297c5169-1f02-4d44-a8c6-2aa7c29e1f83/_identitymd/README.md> |

### Project `b72dfb6a-d2bb-498f-a827-9c16bf14f142`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `b72dfb6a-d2bb-498f-a827-9c16bf14f142` | completed | 2026-10-01 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/identity-md-launches/launch-565-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-565-workflow-contract-stage-context/pull/1> |
| 2/2 | `f472bf73-4394-423d-930b-79aedef155d3` | completed | 2026-10-01 | SOURCE-ONLY CONTINUE — no redeploy, no site, no new economics. Parent job: b8f68a19-42b0-428e-80af-0582d26a2805 (Blocked: protected_invariants / project… | <https://github.com/identity-md-launches/launch-565-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-565-workflow-contract-stage-context/pull/2> |

### Project `22a1e5c7-a34a-4949-be3d-8cb6417d261c`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `22a1e5c7-a34a-4949-be3d-8cb6417d261c` | completed | 2026-09-30 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/identity-md-launches/launch-522-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-522-workflow-contract-stage-context/pull/1> |
| 2/2 | `cbe454a2-ae64-43be-8981-f86bd284cf5c` | completed | 2026-10-01 | CONTINUE job 8c0d9340-589f-42c4-a7e7-a34df94a0662 as a source-only follow-up. Do not deploy, do not host, do not change launch.json addresses, do not open a… | <https://github.com/identity-md-launches/launch-522-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-522-workflow-contract-stage-context/pull/2> |

### Project `4a26aecb-5f31-4474-bdde-7021f71c3b7c`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `4a26aecb-5f31-4474-bdde-7021f71c3b7c` | completed | 2026-09-26 | Lets create a website to buy and sell imd on ethereum mainnet via the uniswap v4 pool | <https://github.com/identity-md-launches/launch-193-lets-create-website-buy> |
| 2/3 | `f57a906e-e020-43f1-843b-560f27e39d45` | completed | 2026-09-29 | lets deploy this as a website to ipfs so we can buy and sell imd on ethereum mainnet. | <https://github.com/identity-md-launches/launch-193-lets-create-website-buy> <https://github.com/identity-md-launches/launch-193-lets-create-website-buy/pull/1> |
| 3/3 | `b76742f1-afb0-48ea-a687-cd3a8e063a9a` | completed | 2026-09-30 | lets change the theme and styling of all the site to match imd.fun and pepe general theme too What the site shows: i mean it's the site about imd | <https://github.com/identity-md-launches/launch-193-lets-create-website-buy> <https://github.com/identity-md-launches/launch-193-lets-create-website-buy/pull/2> |

### Project `5bd893a1-222c-4514-8f45-c32cad489491`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `5bd893a1-222c-4514-8f45-c32cad489491` | completed | 2026-09-30 | Create a polished, shiny, energetic 15-second marketing video for https://pepe2pepe.fun. Explain what the actual product does through beautiful moving shots… | <https://github.com/identity-md-launches/launch-502-create-polished-shiny-energetic> <https://github.com/identity-md-launches/launch-502-create-polished-shiny-energetic/pull/1> <https://pepe2pepe.fun> |
| 2/2 | `e98afbf0-2481-48cd-9280-97fefd7acbd9` | completed | 2026-09-30 | Remake the Pepe2Pepe marketing video as a beautiful, professionally edited 20-second film. Act as a creative director and professional video editor with 25… | <https://github.com/identity-md-launches/launch-502-create-polished-shiny-energetic> <https://github.com/identity-md-launches/launch-502-create-polished-shiny-energetic/pull/2> |

### Project `874ecc59-afcf-4902-91c2-137e4fdafe43`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `874ecc59-afcf-4902-91c2-137e4fdafe43` | completed | 2026-09-29 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/identity-md-launches/launch-468-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-468-workflow-contract-stage-context/pull/1> |
| 2/2 | `47a6e156-a0da-4c71-8d29-80188c93a70e` | completed | 2026-09-29 | Implement the approved 4% GRID fee-on-transfer that the audit flagged as missing. Every transfer and transferFrom must take TAX_BPS = 400 from the sent… | <https://github.com/identity-md-launches/launch-468-workflow-contract-stage-context> <https://github.com/identity-md-launches/launch-468-workflow-contract-stage-context/pull/2> |

### Project `9c1c8867-098d-4b2d-bcb2-71ed1276795f`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `9c1c8867-098d-4b2d-bcb2-71ed1276795f` | completed | 2026-09-28 | Build a polished responsive web application called “SIMCARD” for IdentityMD agents. Core experience: * The homepage must have one prominent search field… | <https://github.com/identity-md-launches/launch-436-build-polished-responsive-web> |
| 2/3 | `88dfb037-d487-4e15-8665-6c59cb60edf6` | completed | 2026-09-29 | Improve the existing SIMCARD website. Do not rebuild it from scratch and do not remove the current animated card, token search, PNG/video download, profile… | <https://github.com/identity-md-launches/launch-436-build-polished-responsive-web> <https://github.com/identity-md-launches/launch-436-build-polished-responsive-web/pull/1> |
| 3/3 | `0b68e3f0-7681-4f52-8a08-05caaf5fb27d` | completed | 2026-09-29 | Update the existing SIMCARD website. Preserve the current visual design, animated NFT card, routes, download buttons, QR code, X sharing, and responsive… | <https://github.com/identity-md-launches/launch-436-build-polished-responsive-web> <https://github.com/identity-md-launches/launch-436-build-polished-responsive-web/pull/2> |

### Project `a10bd012-c45d-4e03-8fcc-1f198aacc21c`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `a10bd012-c45d-4e03-8fcc-1f198aacc21c` | completed | 2026-09-28 | Build and publish a website called: IMDerivatives PURPOSE IMDerivatives is an independent directory of projects, tokens, NFTs, strategies, apps and… | <https://github.com/identity-md-launches/launch-432-build-publish-website-called> |
| 2/2 | `4980b633-b73a-4003-80e8-4a657faeee3e` | completed | 2026-09-29 | Continue and update the existing IMDerivatives website from parent job: a10bd012-c45d-4e03-8fcc-1f198aacc21c Do NOT rebuild an unrelated site. Preserve the… | <https://github.com/identity-md-launches/launch-432-build-publish-website-called> <https://github.com/identity-md-launches/launch-432-build-publish-website-called/pull/1> |

### Project `53b09dd6-cc8d-469c-adc1-9eac85df4f1a`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `53b09dd6-cc8d-469c-adc1-9eac85df4f1a` | blocked | 2026-09-23 | Answer this question about chain 1 over blocks 26041271 to 26041271, exactly as .imd/reads/oracle.json pins it: Should AI companies be allowed to train… | — |
| 2/2 | `7417430a-f20e-42b3-bb0b-e94318085fc1` | completed | 2026-09-24 | Answer this question about chain 1 over blocks 26041271 to 26041271, exactly as .imd/reads/oracle.json pins it: Should AI companies be allowed to train… | — |

### Project `3eb4a46b-1e86-4e81-9678-de24ae7bc0a4`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `3eb4a46b-1e86-4e81-9678-de24ae7bc0a4` | blocked | 2026-09-23 | Answer this question about chain 1 over blocks 26032887 to 26033186, exactly as .imd/reads/oracle.json pins it: What was the total USDC swap volume in… | — |
| 2/2 | `e410f4db-8fcd-4318-9642-a87f96c54c9b` | completed | 2026-09-24 | Answer this question about chain 1 over blocks 26032887 to 26033186, exactly as .imd/reads/oracle.json pins it: What was the total USDC swap volume in… | — |

### Project `6c296b69-8c22-435c-a2c2-56ab1660bb4e`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `6c296b69-8c22-435c-a2c2-56ab1660bb4e` | blocked | 2026-09-23 | Answer this question about chain 1 over blocks 26027267 to 26041556, exactly as .imd/reads/oracle.json pins it: Has the Identity MD NFT collection (OpenSea… | — |
| 2/2 | `850085d8-6973-4244-8511-270db8de90d4` | completed | 2026-09-24 | Answer this question about chain 1 over blocks 26027267 to 26041556, exactly as .imd/reads/oracle.json pins it: Has the Identity MD NFT collection (OpenSea… | — |

### Project `0dd9160e-f13a-4190-ab9a-88d12fbd42e9`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/2 | `0dd9160e-f13a-4190-ab9a-88d12fbd42e9` | blocked | 2026-09-24 | Answer this question about chain 4663 over blocks 71048421 to 71083911, exactly as .imd/reads/oracle.json pins it: Which Uniswap v4 pool on Robinhood Chain… | — |
| 2/2 | `76cc6f6b-6c31-43b2-acef-b4a1463e3baa` | completed | 2026-09-24 | Answer this question about chain 4663 over blocks 71048421 to 71083911, exactly as .imd/reads/oracle.json pins it: Which Uniswap v4 pool on Robinhood Chain… | — |

### Project `722b0171-c574-4c06-8a46-dc4d9349df1f`

| Version | Job id | State | Created | Objective (truncated by API) | Links in record |
|---|---|---|---|---|---|
| 1/3 | `722b0171-c574-4c06-8a46-dc4d9349df1f` | completed | 2026-09-22 | WORKFLOW CONTRACT STAGE CONTEXT: the stage produces implemented and tested contracts, ABI documentation and an independently reviewed launch.json. Each… | <https://github.com/Identity-md/launch-108-proofofworktoken> |
| 2/3 | `5592b20b-43d3-466a-84ab-15b16185201c` | completed | 2026-09-22 | Original request: Repair the existing Proof Of Work claim website and republish to the SAME explicit IPFS hosting label work (work.site.identitymd.eth).… | <https://github.com/Identity-md/launch-110-original-request-repair-existing> |
| 3/3 | `c55b05c8-d2db-4c18-899b-7462d2bc0e5d` | completed | 2026-09-22 | Original request: Build and publicly host WORK2, a clean minimal RainbowKit claim website for the existing WORK token on Sepolia. Use frontend-for-contract… | — |

