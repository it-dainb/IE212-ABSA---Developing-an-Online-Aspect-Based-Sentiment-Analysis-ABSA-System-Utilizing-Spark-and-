products_api = 'https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11036132&limit=100&offset={offset}'
comments_api = 'https://shopee.vn/api/v2/item/get_ratings?exclude_filter=1&filter=1&filter_size=0&flag=1&fold_filter=0&itemid={item_id}&limit={limit}&offset={offset}&relevant_reviews=false&request_source=2&shopid={shop_id}&tag_filter=&type={star}&variation_filters='
import pickle

max_comment = 6_000
total_comment = 0

save_name = 'data/electric'

import requests as req


selection_prop = [
    'itemid',
    'shopid',
    'name',
    'currency',
    'price',
    'price_before_discount',
    'raw_discount',
    'item_rating'
]

selection_cmt_prop = [
    'cmtid',
    'comment',
    'rating_star'
]

def get_products(products_api):
    data = req.get(products_api).json()
    for section in data['data']['sections']:
        for item in section['data']['item']:
            item_data = {}
            for k, v in item.items():
                if v is None:
                    continue

                if k not in selection_prop:
                    continue

                item_data[k] = v
            yield item_data

dict_star = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
}
def get_comments(comments_api, product, comment_per_star = 100):
    
    dict_star_local = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    comment_list = []
    seen_comment = []
    for star in range(1, 6):
        for offset in range(0, comment_per_star, 50):
            request_cmts = comments_api.format(item_id = product['itemid'], shop_id = product['shopid'], limit = 50, offset = offset, star = star)
            product_data = req.get(request_cmts).json()

            try:
                for comment in product_data['data']['ratings']:
                    comment_data = {}
                    for k, v in comment.items():
                        if v is None:
                            continue

                        if k not in selection_cmt_prop:
                            continue

                        comment_data[k] = v

                    if comment_data['comment'] == '':
                        continue
                        
                    if comment_data['comment']  in seen_comment:
                        continue
                    
                    seen_comment.append(comment_data['comment'])
                    comment_list.append(comment_data)
                    dict_star[star] += 1
                    dict_star_local[star] += 1
            except:
                break
    return comment_list, product_data['data']['item_rating_summary'], dict_star_local

offset = 0
products_list = []
while total_comment < max_comment:
    for i, product in enumerate(get_products(products_api.format(offset = offset))):
        print(i)
        product['comment'], product['item_rating_summary'], dict_star_local = get_comments(comments_api, product, comment_per_star = 100)
        
        products_list.append(product)
        
        with open( save_name + ".p", "wb" ) as f:
            pickle.dump(products_list, f)
        
        total_comment += len(product['comment'])
        print(len(product['comment']))
        print(dict_star_local)
        print()
        
        # if total_comment >= max_comment:
        #     break

    with open( save_name + ".p", "wb" ) as f:
        pickle.dump(products_list, f)
    
    offset += 100
    
    print("=" * 50)

with open(save_name + ".p", "wb" ) as f:
        pickle.dump(products_list, f)

print(len(products_list))
print(dict_star)
print(total_comment)

import pickle

with open(save_name + ".p", "rb" ) as f:
    products_list = pickle.load(f)

data_df = {}
print(products_list[0].keys())
print(products_list[0]['comment'][0].keys())

for k, v in products_list[0].items():
    if k in ['comment', 'item_rating_summary', 'item_rating']:
        continue
    if k not in data_df:
        data_df[k] = []

for c_k, c_v in products_list[0]['comment'][0].items():
        if c_k not in data_df:
            data_df[c_k] = []

for i, product in enumerate(products_list):
    for cmt in product['comment']:
        
        if cmt['comment'] == '':
            continue
        
        for c_k, c_v in cmt.items():
            data_df[c_k].append(c_v)
        
        for k, v in product.items():
            if k in ['comment', 'item_rating_summary', 'item_rating']:
                continue
            
            if 'price' in k:
                v = float(v) / 100_000
            
            data_df[k].append(v)

import pandas as pd

for k, v in data_df.items():
    print(k, len(v))

df = pd.DataFrame.from_dict(data_df)
print(df)

df.to_csv(save_name + '.csv', index=False, encoding='utf-8', header=True)