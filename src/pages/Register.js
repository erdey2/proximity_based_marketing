import { useState } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { TextField, Button, Container, Typography, Alert } from "@mui/material";
import axios from "axios";

const schema = yup.object().shape({
  username: yup.string().required("Username is required"),
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup.string().min(6, "Minimum 6 characters").required(),
});

const Register = () => {
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
  });

  const [successMessage, setSuccessMessage] = useState("");

  const onSubmit = async (data) => {
    try {
      const response = await axios.post("http://localhost:8000/api/users/register/", data);
      console.log(response.data);

      // Show success message
      setSuccessMessage("User registered successfully!");

      // Clear form fields
      reset();

      // Hide message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (error) {
      console.error(error.response?.data || "Error registering user");
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>Register</Typography>
      
      {/* Success message */}
      {successMessage && <Alert severity="success">{successMessage}</Alert>}

      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField label="Username" fullWidth margin="normal" {...register("username")} error={!!errors.username} helperText={errors.username?.message} />
        <TextField label="Email" fullWidth margin="normal" {...register("email")} error={!!errors.email} helperText={errors.email?.message} />
        <TextField label="Password" type="password" fullWidth margin="normal" {...register("password")} error={!!errors.password} helperText={errors.password?.message} />
        <Button type="submit" variant="contained" color="primary">Register</Button>
      </form>
    </Container>
  );
};

export default Register;
