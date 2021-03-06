# Prepare Data
import pandas as pd
from lightfm.data import Dataset
from scipy.io import mmwrite


# Data Load
# ratings_source: build_interactions 재료, list of tuples
# --> [(user1, item1), (user2, item5), ... ]
# item_features_source: build_item_features 재료
# --> [(item1, [feature, feature, ...]), (item2, [feature, feature, ...])]
ratings = pd.read_csv('data/ratings.csv')
ratings_source = [(ratings['user_id'][i], ratings['book_id'][i]) for i in range(ratings.shape[0])]

item_meta = pd.read_csv('data/books.csv')
item_meta = item_meta[['book_id', 'authors', 'average_rating', 'original_title']]

item_features_source = [(item_meta['book_id'][i],
                        [item_meta['authors'][i],
                         item_meta['average_rating'][i]]) for i in range(item_meta.shape[0])]

# Construct Data-set
# set, list, pandas series 모두 가능하다.
# 먼저 User/Item Index를 mapping하고, User Features/Item Features를 추가한 후
# occurence 데이터를 fit한다.
# 혹은 scipy.csr_matrix를 바로 fit하는 것도 가능하다.
# 주의: Null 값은 다 채운 후여야 한다.
dataset = Dataset()
dataset.fit(users=ratings['user_id'].unique(),
            items=ratings['book_id'].unique(),
            item_features=item_meta[item_meta.columns[1:]].values.flatten()
            )

print("Num Users: {}, Num Items: {}".format(*dataset.interactions_shape()))
print(dataset.user_features_shape(), dataset.item_features_shape())

interactions, weights = dataset.build_interactions(ratings_source)
item_features = dataset.build_item_features(item_features_source)
# mappings = dataset.mapping()

# Save
# mmwrite('data/interactions.mtx', interactions)
# mmwrite('data/item_features.mtx', item_features)
# mmwrite('data/weights.mtx', weights)