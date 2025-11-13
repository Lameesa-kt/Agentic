const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();

app.use(express.json());

// Load static JSON from data folder
const json1 = require("./data/json1.json");  // CompanyABC - D001149727
const json2 = require("./data/json2.json");  // TechCorp Solutions - D000943665
const json3 = require("./data/json3.json");  // Global Logistics Inc - D300888892

// Map customer_id to deal data from data folder
// customer_id 1 → json1.json (CompanyABC)
// customer_id 2 → json2.json (TechCorp Solutions)
// customer_id 3 → json3.json (Global Logistics Inc)
const customerToDealMap = {
  1: json1,  // CompanyABC - json1.json
  2: json2,  // TechCorp Solutions - json2.json
  3: json3   // Global Logistics Inc - json3.json
};

// ✅ Main endpoint: Get deal by customer ID
app.get("/api/getdeal/customer/:customer_id", (req, res) => {
  const customerId = parseInt(req.params.customer_id);
  
  if (isNaN(customerId)) {
    return res.status(400).json({ error: "Invalid customer_id. Must be a number." });
  }
  
  const deal = customerToDealMap[customerId];
  
  if (!deal) {
    return res.status(404).json({ 
      error: `No deal found for customer_id: ${customerId}`,
      available_customer_ids: Object.keys(customerToDealMap).map(Number)
    });
  }
  
  res.json(deal);
});
// ✅ Three separate GET endpoints
app.get("/api/getdeal/1000", (req, res) => {
  res.json(json2);
});

app.get("/api/getdeal/2000", (req, res) => {
  res.json(json1);
});

app.get("/api/getdeal/3000", (req, res) => {
  res.json(json3);
});

// ✅ POST → Save JSON to /data using only bidNum.json
app.post("/api/adddeal", (req, res) => {
  const deal = req.body;

  // Extract bidNum
  const bidNum = deal?.bidStart?.bidHead?.bidNum;

  if (!bidNum) {
    return res.status(400).json({ error: "bidNum not found in JSON" });
  }

  const fileName = `${bidNum}.json`;
  const filePath = path.join(__dirname, "data", fileName);

  // Save (overwrite if already exists)
  fs.writeFile(filePath, JSON.stringify(deal, null, 2), (err) => {
    if (err) {
      console.error("Error saving JSON:", err);
      return res.status(500).json({ error: "Unable to save file" });
    }

    res.status(201).json({
      message: "Deal saved successfully",
      file: fileName
    });
  });
});

// 404 fallback
app.use((req, res) => {
  res.status(404).json({ error: "Route not found" });
});

const PORT = 3000;

app.listen(PORT, () => {
  console.log(`✅ Mock API running on port ${PORT}`);
});
