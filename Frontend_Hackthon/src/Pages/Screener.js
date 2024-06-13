import React, { useEffect, useState } from "react";
import { Card, Row, Col, Button, Tag } from "antd";
import Headers from "../Components/Header";
import Footer from "../Components/Footer";
import { useNavigate } from "react-router-dom";
import { fetchJobList } from "../Services/JobSeeker";

const layoutStyle = {
  display: "flex",
  flexDirection: "column",
  minHeight: "100vh",
};

const headerStyle = {
  marginBottom: "20px",
};

const mainContentStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "left",
  padding: "25px",
  textAlign: "left",
  marginTop: "20px",
  width: "100%",
};

const cardStyle = {
  width: "100%",
  minHeight: 160,
  margin: "0 auto",
  border: "1px solid #d9d9d9",
  borderRadius: "8px",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  transition: "box-shadow 0.3s ease",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
};

const cardHeaderStyle = {
  fontWeight: "bold",
  fontSize: "16px",
  backgroundColor: "#f5f5f5",
  padding: "10px",
};

const cardBodyStyle = {
  padding: "16px",
};

const cardFooterStyle = {
  display: "flex",
  alignItems: "left",
  justifyContent: "space-between",
  padding: "5px",
  borderTop: "1px solid #f0f0f0",
};

const Screener = () => {
  const [companyDetails, setCompanyDetails] = useState(null);
  const [jobOpenings, setJobOpenings] = useState([]);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleAssessment = (job) => {
    sessionStorage.setItem(`job_id`, JSON.stringify(job.job_id));
    navigate("/assessement");
  };

  useEffect(() => {
    const storedCompany = sessionStorage.getItem("selectedCompany");
    if (storedCompany) {
      const company = JSON.parse(storedCompany);
      setCompanyDetails(company);

      const fetchJobs = async () => {
        try {
          const jobsResponse = await fetchJobList(company.org_id);
          if (jobsResponse && jobsResponse.Success) {
            if (Array.isArray(jobsResponse.jobs_data)) {
              setJobOpenings(jobsResponse.jobs_data);
            } else {
              setError("Invalid job list data format.");
              setJobOpenings([]);
            }
          } else {
            setError("Failed to fetch job list.");
          }
        } catch (err) {
          console.error("Error fetching job list:", err.message);
          setError("Error fetching job list.");
        }
      };

      fetchJobs();
    }
  }, []);

  return (
    <div style={layoutStyle}>
      <div style={headerStyle}>
        <Headers />
      </div>
      <div style={{ height: 30 }}></div>
      <div style={mainContentStyle}>
        {companyDetails ? (
          <>
            <h2>Welcome to {companyDetails.org_name} candidate portal</h2>
            <h4>{companyDetails.org_desc}</h4>
            {error ? (
              <p style={{ color: "red" }}>{error}</p>
            ) : (
              <Row
                gutter={[32, 32]}
                justify="left"
                style={{
                  maxWidth: "1200px",
                  width: "100%",
                  padding: "0 25px",
                  marginTop: "25px",
                }}
              >
                {jobOpenings.length > 0 ? (
                  jobOpenings.map((job) => (
                    <Col
                      key={job.job_id}
                      xs={24}
                      sm={12}
                      md={8}
                      style={{
                        display: "flex",
                        justifyContent: "left",
                        padding: "0 8px",
                      }}
                    >
                      <Card style={cardStyle} hoverable>
                        <div style={cardHeaderStyle}>{job.job_role}</div>
                        <div style={cardBodyStyle}>
                          <p>
                            <b>Req Exp :</b> {job.required_exp} yrs ,{" "}
                            <b>Status:</b> {job.job_status}
                          </p>
                          <p>
                            {job.job_primary_skills
                              .split(",")
                              .map((tech, index) => (
                                <Tag key={index}>
                                  <b>{tech.trim()}</b>
                                </Tag>
                              ))}
                          </p>
                        </div>
                        <div style={cardFooterStyle}>
                          <p>{companyDetails.postedTime}</p>
                          <Button
                            type="primary"
                            onClick={() => handleAssessment(job)}
                          >
                            Apply
                          </Button>
                        </div>
                      </Card>
                    </Col>
                  ))
                ) : (
                  <h5 style={{ marginLeft: "50%", marginTop: "20%" }}>
                    No job openings available for this company.
                  </h5>
                )}
              </Row>
            )}
          </>
        ) : (
          <p>No company selected.</p>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Screener;
