import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropRecommendation.settings')
django.setup()

from CropRecommendationApp.models import Fertilizer

fertilizer_details = {
    "Urea": "Urea is an inexpensive form of nitrogen fertilizer with an NPK ratio of 46-0-0. It promotes rapid green vegetative growth and is highly soluble in water.",
    "DAP": "DAP (Diammonium Phosphate) is the world's most widely used phosphorus fertilizer. It provides excellent root development and early growth support.",
    "14-35-14": "14-35-14 NPK is a complex fertilizer with high phosphorus content. It is ideal for basal application to stimulate strong root systems and flowering.",
    "28-28": "28-28-0 NPK provides equal, high amounts of Nitrogen and Phosphorus. It is highly effective during the early stages of crop growth for rapid establishment.",
    "17-17-17": "17-17-17 NPK is a balanced complex fertilizer that provides an even distribution of primary nutrients, ensuring comprehensive plant health and yield.",
    "20-20": "20-20-0 NPK offers a strong start for crops requiring high nitrogen and phosphorus, improving vegetative growth and root establishment.",
    "10-26-26": "10-26-26 NPK is rich in phosphorus and potassium. It is particularly beneficial during the fruiting and grain-filling stages to ensure high yield quality.",
    "SSP": "Single Super Phosphate (SSP) is an excellent source of Phosphorus, Calcium, and Sulfur. It helps in rapid early root development.",
    "MOP": "Muriate of Potash (MOP) provides potassium, an essential nutrient for plant growth, disease resistance, and fruit quality.",
    "Ammonium Sulphate": "Ammonium Sulphate provides Nitrogen and Sulfur. It is particularly effective for alkaline soils and lowering soil pH.",
    "NPK 19-19-19": "NPK 19-19-19 is a balanced complex fertilizer that provides an even distribution of primary nutrients.",
    "Potassium Sulphate": "Potassium Sulphate is a premium potassium fertilizer ideal for chloride-sensitive crops.",
    "Organic Compost": "Organic Compost improves soil structure, water-holding capacity, and provides a slow release of nutrients.",
    "Organic Manure": "Organic Manure is a rich source of carbon and beneficial microbes, highly recommended for organic farming.",
    "Potash": "Potash fertilizers supply potassium, critical for strong stems, deep roots, and disease resistance.",
    "Vermicompost": "Vermicompost is an organic fertilizer produced by earthworms, rich in water-soluble nutrients.",
    "NPK 12-32-16": "NPK 12-32-16 provides a high dose of Phosphorus and Potassium, great for Sugarcane and similar cash crops.",
    "NPK 20-20-20": "NPK 20-20-20 is a perfectly balanced fertilizer ideal for high-nutrient demanding crops like Banana and Orange.",
    "Super Phosphate": "Super Phosphate is a fantastic source of Phosphorus, essential for seed development and early root formation.",
    "Compost": "Compost is decomposed organic matter that greatly improves soil health, structure, and water retention.",
    "Magnesium Sulphate": "Magnesium Sulphate provides Magnesium and Sulfur, crucial for chlorophyll production and treating yellowing leaves.",
    "Gypsum": "Gypsum provides Calcium and Sulfur, improving soil structure and neutralizing soil toxicity without affecting pH.",
    "Organic Fertilizer": "Organic Fertilizer releases nutrients slowly and naturally, improving long-term soil fertility and health."
}

for name, description in fertilizer_details.items():
    obj, created = Fertilizer.objects.get_or_create(name=name)
    obj.description = description
    obj.save()
    print(f"Saved: {name}")

print("Successfully populated the Fertilizer database!")

print("--------------------------------------------------")
print("Starting Fertilizer Image Migration...")

import shutil
import glob

brain_dir = r"C:\Users\avina\.gemini\antigravity\brain\347d7afa-6ca8-40e1-ab73-bd25622bb5f2"
static_dir = r"d:\project ambu\Crop-Recommendation-main\CropRecommendationApp\static\fertilizers"

if not os.path.exists(static_dir):
    os.makedirs(static_dir)

fertilizers = [
    "urea", "npk_20_20_20", "dap", "npk_12_32_16", "super_phosphate",
    "organic_manure", "vermicompost", "ssp", "potash", "npk_19_19_19",
    "organic_compost", "potassium_sulphate", "magnesium_sulphate",
    "ammonium_sulphate", "gypsum", "compost", "organic_fertilizer"
]

for fert in fertilizers:
    pattern = os.path.join(brain_dir, f"{fert}_*.png")
    matches = glob.glob(pattern)
    if matches:
        latest = max(matches, key=os.path.getctime)
        dest = os.path.join(static_dir, f"{fert}.png")
        shutil.copy2(latest, dest)
        print(f"Copied {fert} image to static directory.")
    else:
        print(f"Missing image for: {fert}")

print("Done copying fertilizer images. Setup Complete!")
