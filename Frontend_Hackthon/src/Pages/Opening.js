import React, { useEffect, useState } from "react";
import { Card, Row, Col } from "antd";
import { useNavigate } from "react-router-dom";
import Headers from "../Components/Header";
import Footer from "../Components/Footer";

// Card styles
const cardStyle = {
  width: 400,
  maxHeight: 290,
  margin: "16px",
  textAlign: "center",
  cursor: "pointer",
  border: "1px solid #d9d9d9",
  borderRadius: "8px",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  transition: "box-shadow 0.3s ease",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
};

const cardContentStyle = {
  padding: "16px",
};

const cardFooterStyle = {
  textAlign: "right",
  color: "#999",
  fontSize: "12px",
  borderTop: "1px solid #f0f0f0",
  padding: "8px",
  marginTop: "auto",
};

// Container styles
const containerStyle = {
  padding: "50px 50px 0 50px",
  flexGrow: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "left",
  marginTop: "20px",
};

const headerStyle = {
  marginBottom: "20px",
};

const layoutStyle = {
  display: "flex",
  flexDirection: "column",
  minHeight: "100vh",
};

const mainContentStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "left",
};

const Opening = () => {
  const navigate = useNavigate();
  const [organizationsData, setOrganizationsData] = useState([]);
  const [username, setUsername] = useState("");

  useEffect(() => {
    const data = sessionStorage.getItem("userData");

    if (data) {
      const parsedData = JSON.parse(data);
      const enrichedData = (parsedData.organizations_data || []).map((org) => ({
        ...org,
        postedTime: "Posted 5 days ago", // Add posted time information here
      }));
      setOrganizationsData(enrichedData);
      setUsername(parsedData.username || "User");
    }
  }, []);

  const handleCardClick = (companyDetails) => {
    sessionStorage.setItem("selectedCompany", JSON.stringify(companyDetails));
    navigate("/screener");
  };

  return (
    <div style={layoutStyle}>
      <div style={headerStyle}>
        <Headers />
      </div>
      <div style={mainContentStyle}>
        <div style={containerStyle}>
          <div>
            <h1>Welcome, {username}</h1>
          </div>
          <Row gutter={[16, 16]} justify="center">
            {organizationsData.length > 0 ? (
              organizationsData.map((opening) => (
                <Col key={opening.org_id} lg={6}>
                  <Card
                    style={cardStyle}
                    onClick={() => handleCardClick(opening)}
                    hoverable
                  >
                    <div style={cardContentStyle}>
                      <h3>{opening.org_name || "No Name Available"}</h3>
                      <p>{opening.org_desc || "No description available."}</p>
                    </div>
                    <div style={cardFooterStyle}>
                    
                      <p>{opening.postedTime}</p> {/* Display posted time */}
                    </div>
                  </Card>
                </Col>
              ))
            ) : (
              <p>No openings available at this time.</p>
            )}
          </Row>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Opening;
