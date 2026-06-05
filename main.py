import heapq

# =========================
# PRODUCT CLASS
# =========================
class Product:
    def __init__(self, pid, name, category, rating):
        self.pid = pid
        self.name = name
        self.category = category
        self.rating = rating


# =========================
# USER CLASS
# =========================
class User:
    def __init__(self, uid):
        self.uid = uid
        self.purchased = []
        self.searched = []
        self.cart = []


# =========================
# RECOMMENDATION ENGINE
# =========================
class RecommendationEngine:
    def __init__(self):
        self.products = {}   # HashMap for products
        self.users = {}      # HashMap for users

    # Add product
    def add_product(self, product):
        self.products[product.pid] = product

    # Add user
    def add_user(self, user):
        self.users[user.uid] = user

    # -------------------------
    # SIMILARITY FUNCTION
    # -------------------------
    def similarity_score(self, user, product):
        score = 0

        # 1. Category match from purchased items
        for pid in user.purchased:
            if pid in self.products:
                if self.products[pid].category == product.category:
                    score += 5

        # 2. Search history boost
        if product.name in user.searched:
            score += 3

        # 3. Cart priority boost (very strong signal)
        if product.pid in user.cart:
            score += 10

        # 4. Rating importance
        score += product.rating

        return score

    # -------------------------
    # GET RECOMMENDATIONS
    # -------------------------
    def recommend(self, uid, top_n=3):
        if uid not in self.users:
            return []

        user = self.users[uid]

        heap = []

        for pid, product in self.products.items():

            # Skip already purchased
            if pid in user.purchased:
                continue

            score = self.similarity_score(user, product)

            # max heap using negative score
            heapq.heappush(heap, (-score, product.name))

        results = []

        while heap and len(results) < top_n:
            results.append(heapq.heappop(heap)[1])

        return results

    # -------------------------
    # SHOW ALL PRODUCTS
    # -------------------------
    def show_products(self):
        print("\n📦 PRODUCT LIST:")
        for p in self.products.values():
            print(f"{p.pid} | {p.name} | {p.category} | ⭐{p.rating}")


    # -------------------------
    # SHOW USER DATA
    # -------------------------
    def show_user(self, uid):
        user = self.users[uid]
        print("\n👤 USER DATA:")
        print("Purchased:", user.purchased)
        print("Searched:", user.searched)
        print("Cart:", user.cart)


# =========================
# MAIN PROGRAM (SIMULATION)
# =========================
def main():

    engine = RecommendationEngine()

    # -------------------------
    # PRODUCTS (DATASET)
    # -------------------------
    engine.add_product(Product(1, "Shoes", "Fashion", 4))
    engine.add_product(Product(2, "Watch", "Fashion", 5))
    engine.add_product(Product(3, "Laptop", "Electronics", 5))
    engine.add_product(Product(4, "Phone", "Electronics", 4))
    engine.add_product(Product(5, "Bag", "Fashion", 3))
    engine.add_product(Product(6, "Headphones", "Electronics", 4))
    engine.add_product(Product(7, "T-Shirt", "Fashion", 4))

    # -------------------------
    # USER DATA
    # -------------------------
    user = User(101)
    user.purchased = [1]          # Shoes already bought
    user.searched = ["Watch"]     # searched Watch
    user.cart = [2]               # Watch in cart

    engine.add_user(user)

    # -------------------------
    # CLI MENU
    # -------------------------
    while True:
        print("\n==============================")
        print(" E-COMMERCE RECOMMENDATION ENGINE ")
        print("==============================")
        print("1. Show Products")
        print("2. Show User Data")
        print("3. Get Recommendations")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            engine.show_products()

        elif choice == "2":
            engine.show_user(101)

        elif choice == "3":
            print("\n🔥 TOP RECOMMENDATIONS:")
            recs = engine.recommend(101, 3)
            for r in recs:
                print("➡", r)

        elif choice == "4":
            print("Exiting... Bye 👋")
            break

        else:
            print("Invalid choice!")


# Run program
if __name__ == "__main__":
    main()