# NoSQL Analysis - FlexiMart

## Section A: Limitations of RDBMS 

A traditional relational database can struggle when product attributes vary a lot across categories. For example, laptops need columns like RAM, storage and processor, while shoes need size, color and material. In a single products table this usually creates many nullable columns, or forces us to build separate tables for every category, which makes the schema complex and harder to maintain. When a new product type is added with new attributes, the relational schema often needs to be altered, which is risky and time-consuming in production systems.

Storing customer reviews with details such as user, rating, comment and timestamps is also less natural in a normalized relational design. Reviews typically have a flexible, nested structure and are best represented as arrays of objects. In an RDBMS, modeling them requires additional review tables and multiple joins between products, reviews and users. This increases query complexity and may impact performance, especially when reading product details together with many reviews.

## Section B: NoSQL Benefits with MongoDB 

MongoDB, as a document-oriented NoSQL database, solves many of these problems using a flexible schema. Each product is stored as a JSON-like document, so different products can have different sets of fields. Electronics documents can include attributes like ram and storage, while shoes can include size and color, without forcing every product to have all possible columns. This keeps the data model closer to the business reality and avoids sparse tables full of NULL values.

MongoDB also supports embedded documents and arrays. Product specifications can be stored in a specs sub-document, and reviews can be stored as an embedded reviews array inside the same product document. This lets the application fetch a product together with its reviews in a single query, reducing the need for joins. In addition, MongoDB supports horizontal scalability through sharding, which allows a large and growing product catalog to be distributed across multiple nodes, improving performance and availability.

## Section C: Trade-offs of Using MongoDB

Using MongoDB instead of MySQL introduces some trade-offs. First, enforcing strong relationships and constraints, such as foreign keys, is weaker in MongoDB, so more responsibility moves to the application code to keep data consistent. Complex multi-collection joins are also not as straightforward as SQL joins. Second, although MongoDB supports transactions, relational databases are often more mature for strict ACID guarantees across many tables. Reporting and ad-hoc analytical queries may require extra tools or data pipelines. Finally, development teams that are comfortable with SQL need time to learn MongoDB’s query language and document-modeling best practices.
