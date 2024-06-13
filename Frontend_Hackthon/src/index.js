import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "../src/Controls/LoginPage";
import Screener from "../src/Pages/Screener";
import "./index.css";
import "mdb-react-ui-kit/dist/css/mdb.min.css";

import App from "./App";
import reportWebVitals from "./reportWebVitals";
import Opening from "./Pages/Opening";
import Assessement from "./Pages/Assessement";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
       
        <Route path="/" element={<LoginPage />} />
        <Route path="/screener" element={<Screener />} />
        <Route path="/openings" element={<Opening />} />
        <Route path="/assessement" element={<Assessement />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
