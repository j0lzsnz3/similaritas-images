class Result:
    def __init__(self, compared_with, similarity, img_url):
        self.compared_with = compared_with
        self.similarity = similarity
        self.img_url = img_url

    def toJSON(self):
        return {
            'compared_with': self.compared_with,
            'similarity': self.similarity,
            'img_url': self.img_url
        }
