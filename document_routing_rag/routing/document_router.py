import os
import json
import numpy as np
import faiss

ROUTER_DIR = "indexes/router"

DOC_FOLDER_MAP = {
    "behavior_guide": "behavior",
    "data_access_rules": "data_access",
    "domine_detail": "domain_detail",
    "edge_cases": "edge_cases",
    "tone_style": "tone_style",
}

def build_router_index(doc_ids, doc_centroids):
    os.makedirs(ROUTER_DIR, exist_ok=True)

    dimension = doc_centroids[0].shape[0]
    router_index = faiss.IndexFlatL2(dimension)
    router_index.add(np.array(doc_centroids).astype("float32"))

    faiss.write_index(router_index, os.path.join(ROUTER_DIR, "index.faiss"))

    router_map = {str(i): doc_ids[i] for i in range(len(doc_ids))}
    with open(os.path.join(ROUTER_DIR, "map.json"), "w") as f:
        json.dump(router_map, f, indent=2)


def load_router_index():
    router_index = faiss.read_index(os.path.join(ROUTER_DIR, "index.faiss"))
    with open(os.path.join(ROUTER_DIR, "map.json")) as f:
        router_map = json.load(f)
    return router_index, router_map


def route_query(query_embedding):
    router_index, router_map = load_router_index()

    distances, indices = router_index.search(query_embedding, k=1)
    best_position = int(indices[0][0])
    doc_id = router_map[str(best_position)]
    folder_name = DOC_FOLDER_MAP[doc_id]
    distance = float(distances[0][0])

    return doc_id, folder_name, distance