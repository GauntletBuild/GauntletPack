set -e
cp -r ~/MinecraftModding/custom_entity_gen/out/models/* assets/custom_entity/models/
cp -r ~/MinecraftModding/custom_entity_gen/out/textures/* assets/custom_entity/textures/item
cp -r ~/MinecraftModding/custom_entity_gen/out/item_models/* assets/large_item/models/
cp -r ~/MinecraftModding/custom_entity_gen/out/item_textures/* assets/large_item/textures/item/
cp ~/MinecraftModding/custom_entity_gen/out/stick.json assets/minecraft/models/item/stick.json
zip -r GauntletPack.zip .
mv GauntletPack.zip ~/MinecraftModding/Axiom/versions/1.20.6-fabric/run/resourcepacks
