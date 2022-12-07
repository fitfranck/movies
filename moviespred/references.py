import os

paths = dict(
    project=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
paths['images_raw'] = os.path.join(paths["project"], 'images_raw')
paths['images_train'] = os.path.join(paths["project"], 'images_train')
paths['references'] = os.path.join(paths["project"], 'references')
paths['models'] = os.path.join(paths["project"], 'models')
paths['checkpoints'] = os.path.join(paths["project"], 'checkpoint')

genres_raw = [{
    'id': 28,
    'name': 'Action'
}, {
    'id': 12,
    'name': 'Adventure'
}, {
    'id': 16,
    'name': 'Animation'
}, {
    'id': 35,
    'name': 'Comedy'
}, {
    'id': 80,
    'name': 'Crime'
}, {
    'id': 99,
    'name': 'Documentary'
}, {
    'id': 18,
    'name': 'Drama'
}, {
    'id': 10751,
    'name': 'Family'
}, {
    'id': 14,
    'name': 'Fantasy'
}, {
    'id': 36,
    'name': 'History'
}, {
    'id': 27,
    'name': 'Horror'
}, {
    'id': 10402,
    'name': 'Music'
}, {
    'id': 9648,
    'name': 'Mystery'
}, {
    'id': 10749,
    'name': 'Romance'
}, {
    'id': 878,
    'name': 'Science Fiction'
}, {
    'id': 10770,
    'name': 'TV Movie'
}, {
    'id': 53,
    'name': 'Thriller'
}, {
    'id': 10752,
    'name': 'War'
}, {
    'id': 37,
    'name': 'Western'
}]

genres_list = [
    'action', 'adventure', 'animation', 'comedy', 'crime', 'documentary',
    'drama', 'family', 'fantasy', 'history', 'horror', 'music', 'mystery',
    'romance', 'science-fiction', 'thriller', 'war', 'western'
]
