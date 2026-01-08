// Use FlexiMart database
fleximart;

// ----------------------------------------------------
// Operation 1: Load Data
// ----------------------------------------------------
// JSON file: part2-nosql/products_catalog.json
// Import command to run in terminal (not inside JS):
// mongoimport --db=fleximart --collection=products --file=part2-nosql/products_catalog.json --jsonArray

// ----------------------------------------------------
// Operation 2: Basic Query
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
// ----------------------------------------------------
db.products.find(
    {
        category: "Electronics",
        price: { $lt: 50000 }
    },
    {
        _id: 0,
        name: 1,
        price: 1,
        stock: 1
    }
);

// ----------------------------------------------------
// Operation 3: Review Analysis
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
// ----------------------------------------------------
db.products.aggregate([
    { $unwind: "$reviews" },
    {
        $group: {
            _id: "$product_id",
            name: { $first: "$name" },
            category: { $first: "$category" },
            avg_rating: { $avg: "$reviews.rating" }
        }
    },
    {
        $match: {
            avg_rating: { $gte: 4.0 }
        }
    }
]);

// ----------------------------------------------------
// Operation 4: Update Operation
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
// ----------------------------------------------------
db.products.updateOne(
    { product_id: "ELEC001" },
    {
        $push: {
            reviews: {
                user: "U999",
                rating: 4,
                comment: "Good value",
                date: new Date()
            }
        }
    }
);

// ----------------------------------------------------
// Operation 5: Complex Aggregation
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
// ----------------------------------------------------
db.products.aggregate([
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 }
        }
    },
    {
        $project: {
            _id: 0,
            category: "$_id",
            avg_price: 1,
            product_count: 1
        }
    },
    {
        $sort: { avg_price: -1 }
    }
]);
