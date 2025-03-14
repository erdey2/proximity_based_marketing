import { useState, useEffect } from "react";
import axios from "axios";
import { TextField, Button, Container, Typography, List, ListItem, ListItemText } from "@mui/material";

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  console.log('products', products);

  const fetchProducts = async () => {
    const response = await axios.get("http://localhost:8000/api/products/");
    setProducts(response.data);
  };

  const handleAddProduct = async () => {
    await axios.post("http://localhost:8000/api/products/", { name, price });
    fetchProducts();
  };

  return (
    <Container>
      <Typography variant="h4">Manage Products</Typography>
      <TextField
        label="Product Name"
        fullWidth
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <TextField
        label="Price"
        type="number"
        fullWidth
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        sx={{ marginBottom: 1 }} // Adds space between Price and Add Product button
      />
      <Button
        onClick={handleAddProduct}
        variant="contained"
        color="primary"
        sx={{ marginTop: 1 }} // Optional: Adds space between the button and other content
      >
        Add Product
      </Button>

      <List>
        {products.map((product) => (
          <ListItem key={product.id}>
            <ListItemText primary={`${product.name} - $${product.price}`} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default ProductManagement;

