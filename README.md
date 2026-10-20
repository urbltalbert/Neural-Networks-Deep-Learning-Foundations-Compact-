# Museum guide: artwork genre classification

## Data

WikiArt subset (`huggan/wikiart`, revision `d559852d`): 5 genres x 300 images, 128 x 128 px.
Classes: cityscape, landscape, portrait, religious_painting, still_life.

The images are not in this repository (WikiArt licence). To rebuild the exact same subset:

```bash
pip install "datasets>=3.0" pillow
python make_wikiart_subset.py --label genre --classes portrait landscape cityscape still_life religious_painting --per-class 300 --size 128 --out data/wikiart_genre5
```
