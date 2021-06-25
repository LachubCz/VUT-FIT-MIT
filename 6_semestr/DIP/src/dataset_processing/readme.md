# Vytváření soft-labels trénovacích datasetů

## Zpracování read datasetu
1. ```python add_confidences.py --input read.trn --output read_conf.trn``` - přidání jistot

## Zpracování anotovaného Bentham datasetu (small)
1. ```python add_confidences.py --input bentham_35.trn --output bentham_35_conf.trn``` - přidání jistot

## Zpracování anotovaného Bentham datasetu (big)
1. ```python add_confidences.py --input bentham_350.trn --output bentham_350_conf.trn``` - přidání jistot
2. ```python duplicate_lines.py --input bentham_350_conf.trn --output bentham_350_conf_10.trn --count 10``` - duplikace řádků

## Zpracování váhovaného trénovacího datasetu
1. ```python create_weighted_dataset.py --config config.ini --input-file-path ./unannotated/dataset.ann --lmdb ./unannotated/lines_40.lmdb --output-file-path dataset.txt``` - získání datasetu s 16 variantami
2. ```python select_variations.py --input-file dataset.txt --output-file dataset_selected.txt --threshold 0.9``` - výběr nejjistějších variant
3. ```python merge_datasets.py --first read_conf.trn --second bentham_conf.trn --third dataset_selected.txt --output dataset_ready.trn``` - spojení trénovacích datasetů

## Zpracování zarovnaného trénovacího datasetu
1. ```python create_weighted_dataset.py --config config.ini --input-file-path ./unannotated/dataset.ann --lmdb ./unannotated/lines_40.lmdb --output-file-path dataset.txt``` - získání datasetu s 16 variantami
2. ```python create_aligned_dataset.py --config config.ini --input-file-path dataset.txt --lmdb ./unannotated/lines_40.lmdb --output-file-path dataset_aligned.txt --limit 8``` - získání zarovnaného datasetu
