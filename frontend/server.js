const express = require("express");
const path = require("path");
const axios = require("axios");
const bodyParser = require("body-parser");

const app = express();
const PORT = process.env.PORT || 3000;

// Backend URL comes from environment variable set in docker-compose.yml.
// Falls back to localhost for running frontend standalone outside Docker.
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

// Show the form
app.get("/", (req, res) => {
  res.render("index", { result: null, error: null });
});

// Handle form submission -> forward to Flask backend
app.post("/submit", async (req, res) => {
  const { name, email, message } = req.body;

  try {
    const response = await axios.post(`${BACKEND_URL}/submit`, {
      name,
      email,
      message
    });

    res.render("index", { result: response.data, error: null });
  } catch (err) {
    console.error("Error contacting backend:", err.message);
    const errorMsg =
      err.response?.data?.error ||
      err.response?.data?.message ||
      "Could not reach the Flask backend. Please try again.";
    res.render("index", { result: null, error: errorMsg });
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "Express Frontend" });
});

app.listen(PORT, () => {
  console.log(`🚀 Express frontend running on http://localhost:${PORT}`);
  console.log(`➡️  Forwarding form submissions to backend at ${BACKEND_URL}`);
});
