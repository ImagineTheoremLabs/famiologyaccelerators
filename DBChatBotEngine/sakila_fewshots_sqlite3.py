few_shots = [{
    "Question": "What is the average rental duration for all movies?",
    "SQLQuery": "SELECT AVG(rental_duration) FROM film;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
    },
    {
    "Question": "List the titles of all movies that are rented out more than 100 times.",
    "SQLQuery": "SELECT f.title FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY f.title HAVING COUNT(r.rental_id) > 100;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
    },
    {
    "Question": "Get the name and total rental amount for the customer with the highest rental spending.",
    "SQLQuery": "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id ORDER BY total_spent DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which actor has appeared in the most films?",
    "SQLQuery": "SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id GROUP BY a.actor_id ORDER BY film_count DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "In which films has actress 'Scarlett Johansson' acted?",
    "SQLQuery": "SELECT f.title FROM film f JOIN film_actor fa ON f.film_id = fa.film_id JOIN actor a ON fa.actor_id = a.actor_id WHERE a.first_name = 'Scarlett' AND a.last_name = 'Johansson';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List all movies along with their respective category names.",
    "SQLQuery": "SELECT f.title, c.name FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which actors have acted in 'Action' category movies?",
    "SQLQuery": "SELECT a.first_name, a.last_name FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film_category fc ON fa.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id WHERE c.name = 'Action';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List the top 5 customers by total rental payments.",
    "SQLQuery": "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id ORDER BY total_spent DESC LIMIT 5;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Get the rental count for each movie.",
    "SQLQuery": "SELECT f.title, COUNT(r.rental_id) AS rental_count FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY f.title;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List all actors who have acted in more than 10 movies.",
    "SQLQuery": "SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id GROUP BY a.actor_id HAVING film_count > 10;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find all movies that have been rented more than 50 times.",
    "SQLQuery": "SELECT f.title FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY f.title HAVING COUNT(r.rental_id) > 50;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which stores have the most inventory?",
    "SQLQuery": "SELECT s.store_id, COUNT(i.inventory_id) AS inventory_count FROM store s JOIN inventory i ON s.store_id = i.store_id GROUP BY s.store_id ORDER BY inventory_count DESC;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find all the films that are longer than 2 hours.",
    "SQLQuery": "SELECT title FROM film WHERE length > 120;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List all customers and their rental history.",
    "SQLQuery": "SELECT c.first_name, c.last_name, r.rental_date FROM customer c JOIN rental r ON c.customer_id = r.customer_id;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which films have not been rented out?",
    "SQLQuery": "SELECT f.title FROM film f LEFT JOIN inventory i ON f.film_id = i.film_id LEFT JOIN rental r ON i.inventory_id = r.inventory_id WHERE r.rental_id IS NULL;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Get the details of all payments made by customer 'John Doe'.",
    "SQLQuery": "SELECT p.payment_id, p.amount, p.payment_date FROM customer c JOIN payment p ON c.customer_id = p.customer_id WHERE c.first_name = 'John' AND c.last_name = 'Doe';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which stores have the most active customers?",
    "SQLQuery": "SELECT s.store_id, COUNT(c.customer_id) AS customer_count FROM store s JOIN customer c ON s.store_id = c.store_id WHERE c.active = 1 GROUP BY s.store_id ORDER BY customer_count DESC;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List the total amount spent by each customer.",
    "SQLQuery": "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the film with the highest replacement cost.",
    "SQLQuery": "SELECT title, replacement_cost FROM film ORDER BY replacement_cost DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which films are categorized as 'Horror' and have a rental rate greater than 3.00?",
    "SQLQuery": "SELECT f.title FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id WHERE c.name = 'Horror' AND f.rental_rate > 3.00;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List all customers who have rented 'Drama' category films.",
    "SQLQuery": "SELECT DISTINCT c.first_name, c.last_name FROM customer c JOIN rental r ON c.customer_id = r.customer_id JOIN inventory i ON r.inventory_id = i.inventory_id JOIN film f ON i.film_id = f.film_id JOIN film_category fc ON f.film_id = fc.film_id JOIN category cat ON fc.category_id = cat.category_id WHERE cat.name = 'Drama';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which films have a rental rate less than the average rental rate?",
    "SQLQuery": "SELECT title FROM film WHERE rental_rate < (SELECT AVG(rental_rate) FROM film);",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List the top 3 longest films.",
    "SQLQuery": "SELECT title, length FROM film ORDER BY length DESC LIMIT 3;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the most rented film in the 'Comedy' category.",
    "SQLQuery": "SELECT f.title, COUNT(r.rental_id) AS rental_count FROM film f JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id WHERE c.name = 'Comedy' GROUP BY f.film_id ORDER BY rental_count DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List the names of all customers who have never rented a film.",
    "SQLQuery": "SELECT c.first_name, c.last_name FROM customer c LEFT JOIN rental r ON c.customer_id = r.customer_id WHERE r.rental_id IS NULL;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which staff member has processed the most payments?",
    "SQLQuery": "SELECT s.first_name, s.last_name, COUNT(p.payment_id) AS payment_count FROM staff s JOIN payment p ON s.staff_id = p.staff_id GROUP BY s.staff_id ORDER BY payment_count DESC LIMIT 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which stores have the most film inventory?",
    "SQLQuery": "SELECT s.store_id, COUNT(i.inventory_id) AS inventory_count FROM store s JOIN inventory i ON s.store_id = i.store_id GROUP BY s.store_id ORDER BY inventory_count DESC;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which customers have rented 'Family' category films the most?",
    "SQLQuery": "SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS rental_count FROM customer c JOIN rental r ON c.customer_id = r.customer_id JOIN inventory i ON r.inventory_id = i.inventory_id JOIN film_category fc ON i.film_id = fc.film_id JOIN category cat ON fc.category_id = cat.category_id WHERE cat.name = 'Family' GROUP BY c.customer_id ORDER BY rental_count DESC;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find all customers who have made payments totaling more than $200.",
    "SQLQuery": "SELECT c.first_name, c.last_name, SUM(p.amount) AS total_paid FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id HAVING total_paid > 200;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which actors have acted in the movie 'Academy Dinosaur'?",
    "SQLQuery": "SELECT a.first_name, a.last_name FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE f.title = 'Academy Dinosaur';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the total number of movies rented by each customer.",
    "SQLQuery": "SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS rental_count FROM customer c JOIN rental r ON c.customer_id = r.customer_id GROUP BY c.customer_id;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "List the top 5 films with the highest rental rate.",
    "SQLQuery": "SELECT f.title, f.rental_rate FROM film f ORDER BY f.rental_rate DESC LIMIT 5;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Which customers rented films from store 1?",
    "SQLQuery": "SELECT c.first_name, c.last_name FROM customer c JOIN rental r ON c.customer_id = r.customer_id JOIN inventory i ON r.inventory_id = i.inventory_id WHERE i.store_id = 1;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the average rental rate for films in the 'Documentary' category.",
    "SQLQuery": "SELECT AVG(f.rental_rate) FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id WHERE c.name = 'Documentary';",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the title of the film with the film_id 10.",
    "SQLQuery": "SELECT title FROM film WHERE film_id = 10;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Get the details of the customer with customer_id 5.",
    "SQLQuery": "SELECT * FROM customer WHERE customer_id = 5;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Retrieve the first name and last name of the actor with actor_id 3.",
    "SQLQuery": "SELECT first_name, last_name FROM actor WHERE actor_id = 3;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Get the payment details for payment_id 15.",
    "SQLQuery": "SELECT * FROM payment WHERE payment_id = 15;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Find the category name with category_id 7.",
    "SQLQuery": "SELECT name FROM category WHERE category_id = 7;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
    "Question": "Retrieve the details of the store with store_id 2.",
    "SQLQuery": "SELECT * FROM store WHERE store_id = 2;",
    "SQLResult": "Result of the SQL query",
    "Answer": ""
},
{
        "Question": "List all movies, their categories, and the actors who have acted in them, including the store they are available in.",
        "SQLQuery": """
            SELECT f.title AS movie_title, c.name AS category_name, a.first_name AS actor_first_name, a.last_name AS actor_last_name, s.store_id
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            JOIN inventory i ON f.film_id = i.film_id
            JOIN store s ON i.store_id = s.store_id;
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "Find all customers who have rented movies from the 'Action' category, along with the rental details and staff who processed the rental.",
        "SQLQuery": """
            SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, f.title AS movie_title, r.rental_date, s.first_name AS staff_first_name, s.last_name AS staff_last_name
            FROM customer c
            JOIN rental r ON c.customer_id = r.customer_id
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category cat ON fc.category_id = cat.category_id
            JOIN staff s ON r.staff_id = s.staff_id
            WHERE cat.name = 'Action';
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "List the top 5 rented movies with their category names and the stores they are available in.",
        "SQLQuery": """
            SELECT f.title AS movie_title, c.name AS category_name, s.store_id, COUNT(r.rental_id) AS rental_count
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            JOIN inventory i ON f.film_id = i.film_id
            JOIN store s ON i.store_id = s.store_id
            JOIN rental r ON i.inventory_id = r.inventory_id
            GROUP BY f.title, c.name, s.store_id
            ORDER BY rental_count DESC
            LIMIT 5;
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "Find all movies rented by 'John Doe', along with the rental staff and the store they rented from.",
        "SQLQuery": """
            SELECT f.title AS movie_title, r.rental_date, s.first_name AS staff_first_name, s.last_name AS staff_last_name, st.store_id
            FROM customer c
            JOIN rental r ON c.customer_id = r.customer_id
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            JOIN store st ON i.store_id = st.store_id
            JOIN staff s ON r.staff_id = s.staff_id
            WHERE c.first_name = 'John' AND c.last_name = 'Doe';
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "List the total rental amount by customers in 'San Francisco' along with the movies they rented and the rental staff.",
        "SQLQuery": """
            SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, SUM(p.amount) AS total_rental_amount, f.title AS movie_title, s.first_name AS staff_first_name, s.last_name AS staff_last_name
            FROM customer c
            JOIN address a ON c.address_id = a.address_id
            JOIN city ci ON a.city_id = ci.city_id
            JOIN rental r ON c.customer_id = r.customer_id
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            JOIN payment p ON r.rental_id = p.rental_id
            JOIN staff s ON r.staff_id = s.staff_id
            WHERE ci.city = 'San Francisco'
            GROUP BY c.customer_id, f.title;
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    },
    {
        "Question": "Find all customers who have rented a 'Horror' category movie more than once, along with their rental history and staff involved.",
        "SQLQuery": """
            SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, f.title AS movie_title, r.rental_date, s.first_name AS staff_first_name, s.last_name AS staff_last_name
            FROM customer c
            JOIN rental r ON c.customer_id = r.customer_id
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category cat ON fc.category_id = cat.category_id
            JOIN staff s ON r.staff_id = s.staff_id
            WHERE cat.name = 'Horror'
            GROUP BY c.customer_id, f.title
            HAVING COUNT(r.rental_id) > 1;
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": ""
    }
]