/* jshint esversion: 8 */

const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const cors = require("cors");
const cars = require("./inventory");
const dealerships = require("./dealership");
const reviews = require("./review");

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Connect to MongoDB
const url = "mongodb://localhost:27017/dealership";
mongoose.connect(url, { useNewUrlParser: true, useUnifiedTopology: true });

// Routes

// Get all reviews
app.get("/reviews", async (req, res) => {
  try {
    const allReviews = await reviews.find({});
    res.json(allReviews);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Get all dealerships
app.get("/dealerships", async (req, res) => {
  try {
    const allDealerships = await dealerships.find({});
    res.json(allDealerships);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Get cars by dealer_id
app.get("/cars/:dealer_id", async (req, res) => {
  try {
    const dealerId = req.params.dealer_id;
    const dealerCars = await cars.find({ dealer_id: dealerId });
    res.json(dealerCars);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Add a new review
app.post("/reviews", async (req, res) => {
  try {
    const newReview = new reviews(req.body);
    const savedReview = await newReview.save();
    res.json(savedReview);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Add a new dealership
app.post("/dealerships", async (req, res) => {
  try {
    const newDealership = new dealerships(req.body);
    const savedDealership = await newDealership.save();
    res.json(savedDealership);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Add a new car
app.post("/cars", async (req, res) => {
  try {
    const newCar = new cars(req.body);
    const savedCar = await newCar.save();
    res.json(savedCar);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
