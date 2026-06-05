import streamlit as st
import heapq
from collections import defaultdict, Counter

# =========================
# PRODUCT MODEL
# =========================
class Product:
    def __init__(self, pid, name, category, rating):
        self.pid = pid
        self.name = name
        self.category = category
        self.rating = rating


# =========================
# USER MODEL
# =========================
class User:
    def __init__(self, uid):
        self.uid = uid
        self.purchased = []
        self.searched = []
        self.cart = []


# =========================
# PRODUCTION RECOMMENDATION ENGINE
# =========================
class RecommendationEngine:
    def __init__(self):
        self.products = {}
        self.users = {}
        self.trending_counter = Counter()
        self.co_matrix = defaultdict(lambda: defaultdict(int))

    # -------------------------
    # ADD DATA
    # -------------------------
    def add_product(self, product):
        self.products[product.pid] = product

    def add_user(self, user):
        self.users[user.uid] = user

    # -------------------------
    # BUILD TRENDING DATA
    # -------------------------
    def build_trending(self):
        for user in self.users.values():
            for pid in user.purchased:
                self.trending_counter[pid] += 1

    # -------------------------
    # BUILD COLLABORATIVE DATA
    # -------------------------
    def build_collaborative(self):
        for user in self.users.values():
            for p1 in user.purchased:
                for p2 in user.purchased:
                    if p1 != p2:
                        self.co_matrix[p1][p2] += 1

    # -------------------------
    # CONTENT SCORE
    # -------------------------
    def content_score(self, user, product):
        score = 0

        for pid in user.purchased:
            if pid in self.products:
                if self.products[pid].category == product.category:
                    score += 5

        if product.name in user.searched:
            score += 3

        if product.pid in user.cart:
            score += 10

        score += product.rating * 2

        return score

    # -------------------------
    # COLLABORATIVE SCORE
    # -------------------------
    def collab_score(self, user, product):
        score = 0

        for pid in user.purchased:
            score += self.co_matrix[pid][product.pid]

        return score

    # -------------------------
    # TRENDING SCORE (NEW)
    # -------------------------
    def trending_score(self, product):
        return self.trending_counter[product.pid]

    # -------------------------
    # HYBRID SCORE (UPGRADED)
    # -------------------------
    def final_score(self, user, product):
        return (
            0.5 * self.content_score(user, product) +
            0.3 * self.collab_score(user, product) +
            0.2 * self.trending_score(product)
        )

    # -------------------------
    # RECOMMENDATION ENGINE
    # -------------------------
    def recommend(self, user):
        heap = []

        for pid, product in self.products.items():

            # skip purchased
            if pid in user.purchased:
                continue

            score = self.final_score(user, product)

            heapq.heappush(heap, (-score, product.name, product.category))

        results = []

        while heap:
            results.append(heapq.heappop(heap))

        return results


# =========================
# INIT SYSTEM
# =========================
engine = RecommendationEngine()

# PRODUCTS
engine.add_product(Product(1, "Shoes", "Fashion", 4))
engine.add_product(Product(2, "Watch", "Fashion", 5))
engine.add_product(Product(3, "Laptop", "Electronics", 5))
engine.add_product(Product(4, "Phone", "Electronics", 4))
engine.add_product(Product(5, "Bag", "Fashion", 3))
engine.add_product(Product(6, "Headphones", "Electronics", 4))
engine.add_product(Product(7, "T-Shirt", "Fashion", 4))

# USERS
u1 = User(101)
u1.purchased = [1, 2]
u1.searched = ["Watch"]
u1.cart = [2]

u2 = User(102)
u2.purchased = [3, 4]
u2.searched = ["Laptop"]
u2.cart = []

engine.add_user(u1)
engine.add_user(u2)

# BUILD MODELS
engine.build_trending()
engine.build_collaborative()


# =========================
# STREAMLIT UI (UPGRADED)
# =========================
st.set_page_config(page_title="Production Recommendation Engine", layout="wide")

st.title("🛒 Production-Grade Recommendation System")
st.markdown("Hybrid AI + DSA Engine (Content + Collaborative + Trending)")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("Controls")

user_id = st.sidebar.selectbox("Select User", list(engine.users.keys()))

show_products = st.sidebar.checkbox("Show Products")
show_users = st.sidebar.checkbox("Show User Data")

# -------------------------
# SAFE USER FETCH (FIXED)
# -------------------------
user = engine.users.get(user_id, engine.users[101])

# -------------------------
# PRODUCT VIEW
# -------------------------
if show_products:
    st.subheader("📦 Product Catalog")
    for p in engine.products.values():
        st.write(f"{p.pid} | {p.name} | {p.category} | ⭐{p.rating}")

# -------------------------
# USER VIEW
# -------------------------
if show_users:
    st.subheader("👤 User Profile")
    st.write("User ID:", user.uid)
    st.write("Purchased:", user.purchased)
    st.write("Search:", user.searched)
    st.write("Cart:", user.cart)

# -------------------------
# RECOMMENDATIONS
# -------------------------
st.subheader("🔥 Recommendations")

results = engine.recommend(user)

for score, name, category in results[:5]:
    st.success(f"{name} ({category}) → Score: {-score:.2f}")