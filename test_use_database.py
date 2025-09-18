from hloc.utils.database import COLMAPDatabase

database_path = "/home/jennyw2/code/Hierarchical-Localization/outputs/small_engine_on_table/sfm_superpoint+superglue/database.db"

db = COLMAPDatabase.connect(database_path)

import pdb; pdb.set_trace()

# This database is populated and used in reconstruction.py, which is too late in the pipeline I think
# Should actually modify features in global-feats-netvlad.h5