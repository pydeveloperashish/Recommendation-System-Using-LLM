import pandas as pd

# Expanded sample data for products
product_data = [
    {"ID": 1, "Product Name": "Shopify", "Description": "An ecommerce platform that allows you to create and manage an online store. Great for setting up a pet food store.", "Product Tags": "ecommerce, online store, pet food", "Platform": "Ruby on Rails"},
    {"ID": 2, "Product Name": "Magento", "Description": "A powerful ecommerce solution with a lot of customization options. Ideal for a pet food shop with extensive product catalogs.", "Product Tags": "ecommerce, customizable, pet food", "Platform": "PHP"},
    {"ID": 3, "Product Name": "WooCommerce", "Description": "A WordPress plugin that turns your site into a full-featured ecommerce store. Perfect for selling pet food.", "Product Tags": "ecommerce, WordPress, pet food", "Platform": "WordPress"},
    {"ID": 4, "Product Name": "PrestaShop", "Description": "An open-source ecommerce platform with a wide range of features. Good for creating a pet food shop.", "Product Tags": "ecommerce, open-source, pet food", "Platform": "PHP"},
    {"ID": 5, "Product Name": "BigCommerce", "Description": "A cloud-based ecommerce solution for building and managing online stores. Suitable for a pet food store.", "Product Tags": "ecommerce, cloud-based, pet food", "Platform": "SaaS"},
    {"ID": 6, "Product Name": "Drupal Commerce", "Description": "An ecommerce module for Drupal that provides advanced features for online stores. Ideal for pet food ecommerce.", "Product Tags": "ecommerce, Drupal, pet food", "Platform": "Drupal"},
    {"ID": 7, "Product Name": "Joomla VirtueMart", "Description": "An ecommerce extension for Joomla that allows you to set up an online store. Useful for a pet food shop.", "Product Tags": "ecommerce, Joomla, pet food", "Platform": "Joomla"},
    {"ID": 8, "Product Name": "osCommerce", "Description": "An open-source ecommerce solution with a large user base. Good for setting up a pet food store.", "Product Tags": "ecommerce, open-source, pet food", "Platform": "PHP"},
    {"ID": 9, "Product Name": "OpenCart", "Description": "A user-friendly open-source ecommerce platform that supports various store types. Great for a pet food shop.", "Product Tags": "ecommerce, open-source, pet food", "Platform": "PHP"},
    {"ID": 10, "Product Name": "Zencart", "Description": "An open-source ecommerce shopping cart system that offers many features for online stores. Suitable for pet food sales.", "Product Tags": "ecommerce, open-source, pet food", "Platform": "PHP"},
    {"ID": 11, "Product Name": "Wix", "Description": "A cloud-based website builder with ecommerce functionality. Ideal for small to medium-sized pet food stores.", "Product Tags": "website builder, ecommerce, cloud-based", "Platform": "SaaS"},
    {"ID": 12, "Product Name": "Squarespace", "Description": "A website builder with integrated ecommerce tools. Suitable for creating and managing an online pet food store.", "Product Tags": "website builder, ecommerce, customizable", "Platform": "SaaS"},
    {"ID": 13, "Product Name": "Weebly", "Description": "A website builder with ecommerce capabilities. Good for setting up a pet food store with ease.", "Product Tags": "website builder, ecommerce, user-friendly", "Platform": "SaaS"},
    {"ID": 14, "Product Name": "Odoo", "Description": "An open-source suite of business applications including ecommerce. Great for a pet food store with additional business management features.", "Product Tags": "ecommerce, open-source, business management", "Platform": "Python"},
    {"ID": 15, "Product Name": "ECWid", "Description": "A versatile ecommerce platform that integrates with any website. Ideal for adding a pet food store to an existing site.", "Product Tags": "ecommerce, integration, versatile", "Platform": "JavaScript"},
    {"ID": 16, "Product Name": "VirtueMart", "Description": "An ecommerce solution for Joomla, offering flexibility and customization for pet food stores.", "Product Tags": "ecommerce, Joomla, flexible", "Platform": "Joomla"},
    {"ID": 17, "Product Name": "Spree Commerce", "Description": "An open-source ecommerce platform built with Ruby on Rails, offering customization and scalability.", "Product Tags": "ecommerce, open-source, scalable", "Platform": "Ruby on Rails"},
    {"ID": 18, "Product Name": "Solidus", "Description": "A flexible, open-source ecommerce platform built with Ruby on Rails, designed for high-performance online stores.", "Product Tags": "ecommerce, open-source, high-performance", "Platform": "Ruby on Rails"},
    {"ID": 19, "Product Name": "Reaction Commerce", "Description": "An open-source, real-time commerce platform built with Node.js and MongoDB, suitable for modern ecommerce needs.", "Product Tags": "ecommerce, real-time, open-source", "Platform": "Node.js"},
    {"ID": 20, "Product Name": "Gatsby", "Description": "A modern site generator that can be used with ecommerce plugins to create a fast, static online store for pet food.", "Product Tags": "static site, ecommerce, modern", "Platform": "JavaScript"},
    {"ID": 21, "Product Name": "Commerce Cloud", "Description": "A cloud-based ecommerce platform from Salesforce with extensive customization and integration capabilities.", "Product Tags": "ecommerce, cloud-based, Salesforce", "Platform": "SaaS"},
    {"ID": 22, "Product Name": "3dcart", "Description": "An all-in-one ecommerce platform with a range of features for creating and managing online stores.", "Product Tags": "ecommerce, all-in-one, features", "Platform": "SaaS"},
    {"ID": 23, "Product Name": "NopCommerce", "Description": "An open-source ecommerce solution with a wide range of features and a flexible design.", "Product Tags": "ecommerce, open-source, flexible", "Platform": "ASP.NET"},
    {"ID": 24, "Product Name": "Jigoshop", "Description": "A WordPress plugin for ecommerce that offers a range of features for managing online stores.", "Product Tags": "ecommerce, WordPress, plugin", "Platform": "WordPress"},
    {"ID": 25, "Product Name": "AbanteCart", "Description": "An open-source ecommerce solution with a variety of features and extensions.", "Product Tags": "ecommerce, open-source, extensions", "Platform": "PHP"},
    {"ID": 26, "Product Name": "OpenWebAnalytics", "Description": "An open-source web analytics platform that can be integrated with ecommerce stores for tracking and analysis.", "Product Tags": "analytics, open-source, integration", "Platform": "PHP"},
    {"ID": 27, "Product Name": "Kibo Commerce", "Description": "A cloud-based ecommerce platform offering personalized experiences and comprehensive management tools.", "Product Tags": "ecommerce, cloud-based, personalized", "Platform": "SaaS"},
    {"ID": 28, "Product Name": "Nexcess", "Description": "A hosting provider offering specialized services for ecommerce websites, including optimized performance.", "Product Tags": "hosting, ecommerce, performance", "Platform": "SaaS"},
    {"ID": 29, "Product Name": "X-Cart", "Description": "A flexible, open-source ecommerce platform with a range of features and customization options.", "Product Tags": "ecommerce, open-source, flexible", "Platform": "PHP"},
    {"ID": 30, "Product Name": "ZenCart", "Description": "A user-friendly, open-source ecommerce shopping cart system with extensive features.", "Product Tags": "ecommerce, open-source, user-friendly", "Platform": "PHP"},
]

# Convert to DataFrame
df = pd.DataFrame(product_data)

# Save to CSV
df.to_csv('dataset.csv', index=False)

print("Expanded dataset created and saved as 'dataset.csv'.")
