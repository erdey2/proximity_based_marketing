import React from "react";
import AppRoutes from "./routes";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import ProductManagement from "./pages/ProductManagement";
import OrderPlacement from "./pages/OrderPlacement";

function App() {
  return  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/products" element={<ProductManagement />} />
      <Route path="/orders" element={<OrderPlacement />} />
    </Routes>
  </Router>


  
}

export default App;

