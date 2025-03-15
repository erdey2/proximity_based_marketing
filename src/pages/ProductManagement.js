import { useState, useEffect } from "react";
import axios from "axios";
import { TextField, Button, Container, Typography, List, ListItem, ListItemText, Alert } from "@mui/material";
import Login from "./Login"; // Import Login component

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [message, setMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("accessToken"));

  useEffect(() => {
    if (isLoggedIn) {
      fetchProducts();
    }
  }, [isLoggedIn]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/products/");
      setProducts(response.data);
    } catch (error) {
      setMessage("❌ Failed to fetch products.");
    }
  };

  const handleAddProduct = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setMessage("⚠️ Unauthorized: Please log in first.\n");
      return;
    }

    try {
      await axios.post(
        "http://localhost:8000/api/products/add/",
        { name, price },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage("✅ Product added successfully!");
      setName("");  // Clear input fields
      setPrice(""); 
      fetchProducts();
    } catch (error) {
      setMessage("❌ Failed to add product.");
    }
  };

  // 🔹 Handle Logout Function
  const handleLogout = () => {
    localStorage.removeItem("accessToken"); // Remove token from storage
    setIsLoggedIn(false); // Update state to reflect logout
  };

  return (
    <Container>
      {isLoggedIn ? (
        <>
          <Typography variant="h4">Manage Products</Typography>

          {/* 🔹 Logout Button */}
          <Button onClick={handleLogout} variant="contained" color="secondary" sx={{ marginBottom: 2 }}>
            Logout
          </Button>

          {message && <Alert severity="info">{message}</Alert>}

          <TextField label="Product Name" fullWidth value={name} onChange={(e) => setName(e.target.value)} sx={{ marginBottom: 2 }} />
          <TextField label="Price" type="number" fullWidth value={price} onChange={(e) => setPrice(e.target.value)} sx={{ marginBottom: 2 }} />
          <Button onClick={handleAddProduct} variant="contained" color="primary">Add Product</Button>

          <List>
            {products.map((product) => (
              <ListItem key={product.id}>
                <ListItemText primary={`${product.name} - $${product.price}`} />
              </ListItem>
            ))}
          </List>
        </>
      ) : (
        <Login onLoginSuccess={() => setIsLoggedIn(true)} />
      )}
    </Container>
  );
};

export default ProductManagement;
