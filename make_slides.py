"""Build the 10-minute presentation (museum_guide.pptx) from the measured results of the notebooks."""
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide(title, bullets=None, image=None, notes=""):
    s = prs.slides.add_slide(BLANK)
    tb = s.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12), Inches(1)).text_frame
    tb.text = title
    tb.paragraphs[0].font.size, tb.paragraphs[0].font.bold = Pt(32), True
    width = Inches(6.2) if image else Inches(12)
    if bullets:
        tf = s.shapes.add_textbox(Inches(0.6), Inches(1.5), width, Inches(5.5)).text_frame
        tf.word_wrap = True
        for i, b in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text, p.font.size, p.space_after = "• " + b, Pt(20), Pt(10)
    if image:
        s.shapes.add_picture(image, Inches(7.0), Inches(1.5), width=Inches(6.0))
    s.notes_slide.notes_text_frame.text = notes
    return s


slide("Museum guide: genre recognition on WikiArt",
      ["5 genres x 300 paintings, 128 x 128 px (cityscape, landscape, portrait, religious painting, still life)",
       "Split by artist: 1 000 train / 250 validation / 250 test, no artist in two sets",
       "Question of the director: is a neural network worth it on modest kiosk CPUs?"],
      notes="30 s. Present the data and the question. Stress the split by artist: otherwise the network recognises the painter.")
slide("1. Dense network from scratch (m1)",
      ["49 152 - 128 sigmoid - 5: 6.3 million weights for 1 000 images",
       "Test accuracy 0.380 (chance 0.20)",
       "Landscape / cityscape mixed up (21 times); religious paintings recognised 4 times out of 50",
       "Flattening throws away which pixels are neighbours"],
      notes="1 min. Test set measured once. Confusion matrix in notebook 01.")
slide("2. Monitoring and failure diagnosis (m2)",
      ["Train accuracy 0.93 vs validation 0.43 after 30 epochs: gap 0.50 = overfitting",
       "Validation loss best at epoch 4 (1.413), 1.731 at epoch 30",
       "Early stopping (patience 5): gap 0.20, but validation accuracy unchanged (0.420 vs 0.432)",
       "Noisy training loss: learning rate 0.2 too large (not fixed)",
       "Ruled out: nan, flat loss at ln 5 = 1.61"],
      notes="2 min. Diagnosis table of Session 6: symptom, evidence, cause, action. Early stopping avoids memorising but does not teach the genres: the limit is the model.")
slide("3. Pretrained ResNet-18 (m3)",
      ["New head (512 x 5) trained alone, then layer4 fine-tuned with lr 1e-4",
       "Test accuracy 0.772 in m3 (0.796 in the m4 rerun) vs 0.380 for the dense network",
       "Religious paintings: 31/50 instead of 4/50",
       "After fine-tuning: train accuracy 0.998, validation loss goes up: a few epochs are enough"],
      notes="1.5 min. Batch norm kept in eval mode. ImageNet normalisation. The two runs differ by about 6 images; we did not investigate why.")
slide("4. Classical model vs neural networks (m4)",
      ["Classical: colour histograms + HOG + RBF-SVM, chosen on validation",
       "Same split, same 250 test images, 1 CPU thread, HOG included in the latency",
       "Margin of an accuracy on 250 images: about +/- 0.05"],
      image="tradeoff_m4.png",
      notes="2 min. The dense network is worse than the classical model. The pretrained ResNet is 25 points above it.")
slide("Results",
      ["Classical (HOG + SVM): 0.516 | 14.5 MB | 2.4 ms",
       "Dense network: 0.388 | 25.2 MB | 0.5 ms",
       "ResNet-18 frozen + logreg: 0.768 | 44.8 MB | 12.9 ms",
       "ResNet-18 fine-tuned: 0.796 | 44.8 MB | 12.4 ms",
       "Frozen vs fine-tuned: 7 images out of 250, inside the margin"],
      image="confusions_m4.png",
      notes="1 min. Numbers come from results_m4.csv.")
slide("Recommendation to the director",
      ["Yes, a neural network is worth it, but a pretrained one, not one trained from scratch",
       "Start with frozen ResNet-18 + logistic regression: no fine-tuning to maintain, accuracy within the margin of the fine-tuned model",
       "12 ms and 45 MB per photo on one CPU thread: acceptable for a kiosk",
       "Limits: latency measured on a laptop, not on the kiosk; only 5 genres; natural-language search not covered"],
      notes="1.5 min. Re-measure latency on the target hardware before committing.")
prs.save("museum_guide.pptx")
