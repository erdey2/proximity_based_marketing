import React from "react";
import { Link } from "react-router-dom";
import { Container, Typography, Button } from "@mui/material";

const Home = () => {
  return (
    <Container>
      <Typography variant="h4">Welcome to Artisan Market</Typography>
      <Button variant="contained" color="primary" component={Link} to="/register">
        Register
      </Button>
      <Button variant="contained" color="secondary" component={Link} to="/products">
        Manage Products
      </Button>
      <Button variant="contained" component={Link} to="/orders">
        Place Order
      </Button>
    </Container>
  );
};

export default Home;
