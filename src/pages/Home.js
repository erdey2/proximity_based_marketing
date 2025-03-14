import React from "react";
import { Link } from "react-router-dom";
import { Container, Typography, Button, Box } from "@mui/material";

const Home = () => {
  return (
    <Container sx={{ textAlign: "center", marginTop: 4 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to Artisan Market
      </Typography>
      <Box sx={{ display: "flex", justifyContent: "center", gap: 2, flexWrap: "wrap", marginTop: 2 }}>
        <Button variant="contained" color="primary" component={Link} to="/register">
          Register
        </Button>
        <Button variant="contained" color="secondary" component={Link} to="/products">
          Manage Products
        </Button>
        <Button variant="contained" color="success" component={Link} to="/orders">
          Place Order
        </Button>
      </Box>
    </Container>
  );
};

export default Home;


