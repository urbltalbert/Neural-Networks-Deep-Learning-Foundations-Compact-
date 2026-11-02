# Museum guide: artwork genre classification

## Data

WikiArt subset (`huggan/wikiart`, revision `d559852d`): 5 genres x 300 images, 128 x 128 px.
Classes: cityscape, landscape, portrait, religious_painting, still_life.

The images are not in this repository (WikiArt licence). To rebuild the exact same subset:

```bash
pip install -r requirements.txt
python make_wikiart_subset.py --label genre --classes portrait landscape cityscape still_life religious_painting --per-class 300 --size 128 --out data/wikiart_genre5
```

## Notebooks (one per milestone)

| Notebook | Content | Key number |
|---|---|---|
| `01_dense_baseline.ipynb` | Dense network 49 152 - 128 - 5 (6.3 M weights), split by artist | test accuracy 0.380 |
| `02_monitoring_diagnosis.ipynb` | Train/validation curves, overfitting (gap 0.53), early stopping, weight decay, dropout, cosine lr decay, diagnosis table | best epoch 4 of 30; no tool changes the val accuracy beyond the margin |
| `03_pretrained_resnet.ipynb` | ResNet-18 pretrained on ImageNet: new head, then fine-tuning of `layer4` | test accuracy 0.772 |
| `04_classical_vs_neural.ipynb` | Classical model vs dense vs ResNet: accuracy, size on disk, latency on 1 CPU thread | see below |

All notebooks use the same split (seed 0, 1 000 / 250 / 250 images, no artist in two sets) and the same 250 test
paintings, measured once per model.

## Is a neural network worth it on the kiosks? (milestone m4)

Test set of 250 paintings, 95 % margin of about +/- 0.05. Latency: median of 50 predictions of one 128 x 128 image
on **one CPU thread**, including the feature extraction (HOG) for the classical model.

| Model | Test accuracy | Size on disk | Latency / image |
|---|---|---|---|
| Classical: colour histograms + HOG + RBF-SVM | 0.516 | 14.5 MB | 2.4 ms |
| Dense network (from scratch, early stopping) | 0.388 | 25.2 MB | 0.5 ms |
| ResNet-18 frozen + logistic regression | 0.768 | 44.8 MB | 12.9 ms |
| ResNet-18 fine-tuned (head + `layer4`) | 0.796 | 44.8 MB | 12.4 ms |

Reading:

- The dense network built from scratch is **worse than the classical model** (0.388 vs 0.516) and bigger: on 1 000
  images, a neural network without prior knowledge is not worth it.
- A **pretrained** ResNet gains about 25 points over the classical model, far beyond the +/- 0.05 margin.
- Fine-tuning (0.796) vs a frozen ResNet with a logistic regression (0.768): 7 images out of 250, inside the margin.
  The same fine-tuning recipe gave 0.772 in m3 and 0.796 in m4 (about 6 images); we did not investigate the cause, but it shows that differences of this size should not be over-interpreted.
- 12 ms and 45 MB are acceptable for a kiosk that classifies one photo on request. Training the ResNet takes about
  2 minutes on a laptop CPU, no GPU needed.

**Recommendation.** Yes, a neural network is worth it, but a *pretrained* one, not one trained from scratch. For a
small team, start with the frozen ResNet-18 + logistic regression (no fine-tuning to maintain, same accuracy within
the margin), and fine-tune only if the museum collects more labelled images.

**Limits.** Latencies were measured on a laptop (one thread of an Apple-silicon CPU), not on the kiosk: they must be
re-measured on the target hardware before committing. Only genres are tested (5 classes, 128 x 128 px); styles and the
natural-language search (point 2 of the brief) are not covered here.
