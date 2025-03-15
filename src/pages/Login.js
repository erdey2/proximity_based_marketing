import { useState } from "react";
import axios from "axios";
import { TextField, Button, Container, Typography, Alert } from "@mui/material";

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/token/", {
        username,
        password,
      });

      localStorage.setItem("accessToken", response.data.access); // Store token
      setMessage("✅ Login successful!");
      onLoginSuccess(); // Call parent function to update UI
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      setMessage("❌ Invalid username or password.");
    }
  };

  return (
    <Container>
      <Typography variant="h4">Login</Typography>
      {message && <Alert severity={message.startsWith("✅") ? "success" : "error"}>{message}</Alert>}
      <TextField label="Username" fullWidth value={username} onChange={(e) => setUsername(e.target.value)} sx={{ marginBottom: 2 }} />
      <TextField label="Password" type="password" fullWidth value={password} onChange={(e) => setPassword(e.target.value)} sx={{ marginBottom: 2 }} />
      <Button onClick={handleLogin} variant="contained" color="primary">
        Login
      </Button>
    </Container>
  );
};

export default Login;
