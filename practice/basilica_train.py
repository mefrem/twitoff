import basilica

import basilica
sentences = [
    "This is a sentence!",
    "x",
    "I don't think this sentence is very similar at all...",
]

with basilica.Connection('a785c156-9338-9fcd-86c4-b563f1193d0f') as c:
    embeddings = list(c.embed_sentences(sentences))
    # print(list(embeddings)) # [[0.8556405305862427, ...], ...]

from scipy import spatial
print(spatial.distance.cosine(embeddings[0], embeddings[1]))
print(spatial.distance.cosine(embeddings[0], embeddings[2]))
