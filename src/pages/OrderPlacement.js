import { useState } from "react";
import axios from "axios";
import { TextField, Button, Container, Typography } from "@mui/material";

const OrderPlacement = () => {
  const [productID, setProductID] = useState("");
  const [quantity, setQuantity] = useState("");

  const handlePlaceOrder = async () => {
    await axios.post("http://localhost:8000/api/orders/", { product: productID, quantity });
    alert("Order placed!");
  };

  return (
    <Container>
      <Typography variant="h4">Place an Order</Typography>
      <TextField label="Product ID" fullWidth value={productID} onChange={(e) => setProductID(e.target.value)} />
      <TextField label="Quantity" type="number" fullWidth value={quantity} onChange={(e) => setQuantity(e.target.value)} />
      <Button 
      onClick={handlePlaceOrder} 
      variant="contained" 
      color="primary"
      sx={{ marginTop: 1 }}
      >Place Order</Button>
    </Container>
  );
};

export default OrderPlacement;
