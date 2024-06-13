import React, { useState, useEffect } from "react";
import { Layout, Button, Upload, Card } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import Headers from "../Components/Header";
import Footer from "../Components/Footer";
import { useNavigate } from "react-router-dom";
import { uploadResume, submitButton } from "../Services/JobSeeker"; // Import the uploadResume function
import ReactApexChart from "react-apexcharts";
const { Content } = Layout;
const { Dragger } = Upload;

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
  alignItems: "center",
  justifyContent: "center",
  padding: "20px",

  marginLeft: "100px",
};

const contentStyle = {
  textAlign: "center",
  margin: "0 20px",
  padding: "20px",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  borderRadius: "8px",
  backgroundColor: "white",
  width: "100%",
  maxWidth: "1000px",
  maxHeight: "500px",
};

const Assessment = () => {
  const [currentPage, setCurrentPage] = useState(0);
  const [questionList, setQuestionList] = useState([]); // Initialize as an empty array
  const [submitted, setSubmitted] = useState(false);
  const [status, setStatus] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({});
  const [answers, setAnswers] = useState({}); // Hashmap to store answers
  const totalPages = questionList.length + 1;
  const navigate = useNavigate();

  const handleNextPage = () => {
    setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    setCurrentPage(currentPage - 1);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true); // Set loading to true when submission starts

      // Format answers and store in session storage
      const formattedAnswers = questionList.map((question, index) => ({
        question: question,
        ans: answers[index + 1] || "", // Index + 1 because currentPage starts from 1
      }));
      sessionStorage.setItem(
        "assessmentAnswers",
        JSON.stringify(formattedAnswers)
      );

      // Get user ID from sessionStorage
      const userDataString = sessionStorage.getItem("userData");
      const userData = userDataString ? JSON.parse(userDataString) : null;
      const user_id = userData ? userData.username : null;

      // Submit answers and user ID to the backend
      const response = await submitButton(formattedAnswers, user_id);

      if (response && response.Success) {
        setData(response);
        // If submission is successful, set submitted to true
        setSubmitted(true);

        // Remove stored answers from session
        sessionStorage.removeItem("assessmentAnswers");
      } else {
        // If submission fails, handle the error (e.g., display error message)
        console.error("Submission failed:", response.error);
      }
    } catch (error) {
      // Handle any unexpected errors
      console.error("Error submitting assessment:", error);
    } finally {
      setLoading(false); // Reset loading state when submission is complete
    }
  };

  const handleAnswerChange = (e) => {
    const { value } = e.target;
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [currentPage]: value,
    }));
  };

  const isLastPage = currentPage === totalPages - 1;

  // Fetch question list when the component mounts

  const fetchQuestions = async () => {
    const jobId = sessionStorage.getItem("job_id");

    const exampleFile = new File([""], "resume.pdf", {
      type: "application/pdf",
    });
    const userDataString = sessionStorage.getItem("userData");
    const selectedCompany = sessionStorage.getItem("selectedCompany");
    const userData = userDataString ? JSON.parse(userDataString) : null;
    const orgData = selectedCompany ? JSON.parse(selectedCompany) : null;

    const username = userData.username;
    const orgId = orgData.org_id;

    const result = await uploadResume(jobId, exampleFile, orgId, username);
    if (result && result.Success) {
      setQuestionList(result.jobs_data); // Update questionList with fetched data
      setStatus(true);
    } else {
      console.error("Failed to fetch questions.");
      setStatus(false);
    }
  };

  return (
    <div style={layoutStyle}>
      <div style={headerStyle}>
        <Headers />
      </div>
      <div style={mainContentStyle}>
        <Content style={contentStyle}>
          {submitted ? (
            <ThankYouPage metrics={data} />
          ) : (
            <>
              {currentPage === 0 ? (
                <ResumeUpload setQuestionList={setQuestionList} />
              ) : (
                <QuestionPage
                  currentPage={currentPage}
                  questionList={questionList}
                  handleAnswerChange={handleAnswerChange}
                />
              )}
              <div
                style={{
                  marginTop: "50px",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                {!isLastPage && currentPage !== 0 && (
                  <Button type="primary" onClick={handleNextPage}>
                    Next
                  </Button>
                )}
                {isLastPage && currentPage !== 0 && (
                  <Button
                    type="primary"
                    onClick={!loading ? handleSubmit : null}
                  >
                    {loading ? "Submitting..." : "Submit"}
                  </Button>
                )}
              </div>
              {currentPage === 0 && (
                <Button
                  type="primary"
                  onClick={handleNextPage}
                  disabled={questionList.length === 0}
                >
                  Start Test
                </Button>
              )}
            </>
          )}
        </Content>
      </div>
      <Footer />
    </div>
  );
};

export default Assessment;

const ResumeUpload = ({ setQuestionList }) => {
  const props = {
    name: "file",
    multiple: false,
    customRequest: async (options) => {
      const { file, onSuccess, onError } = options;
      const user_name = sessionStorage.getItem("userData")
        ? JSON.parse(sessionStorage.getItem("userData")).username
        : null;
      const org_id = sessionStorage.getItem("selectedCompany")
        ? JSON.parse(sessionStorage.getItem("selectedCompany")).org_id
        : null;
      const job_id = sessionStorage.getItem("job_id");
      try {
        const response = await uploadResume(job_id, file, org_id, user_name);
        if (response && response.Success) {
          setQuestionList(response.jobs_data); // Set the fetched questions
          onSuccess(null, file);
        } else {
          onError(new Error("Failed to upload file."));
        }
      } catch (error) {
        onError(error);
      }
    },
  };

  return (
    <Card
      title="Upload Your Resume"
      style={{ width: "90%", marginTop: 40, marginLeft: 30 }}
    >
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">
          Click or drag file to this area to upload
        </p>
      </Dragger>
    </Card>
  );
};

const QuestionPage = ({ currentPage, questionList, handleAnswerChange }) => {
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    // Reset input value when currentPage changes
    setInputValue("");
  }, [currentPage]);

  return (
    <>
      <h2>Question {currentPage}</h2>
      <Card>
        <h5>
          <b>{questionList[currentPage - 1]}</b>
        </h5>
        <input
          type="text"
          style={{
            height: 200,
            width: "100%",
            fontSize: "20px",
            marginTop: "20px",
          }}
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            handleAnswerChange(e);
          }}
        />
      </Card>
    </>
  );
};

const ThankYouPage = ({ metrics }) => {
  // Extract metrics data from props
  const { metrics_dict } = metrics;
  const selectedData = sessionStorage.getItem("selectedCompany");
  const selectedCompany = selectedData ? JSON.parse(selectedData) : null;
  const org = selectedCompany ? selectedCompany.org_name : "";
  const job_id = sessionStorage.getItem("job_id");
  // Define data for the charts
  const barChartData = {
    series: [
      {
        name: "Metrics",
        data: Object.values(metrics_dict), // Use values from metrics_dict
      },
    ],
    options: {
      chart: {
        type: "bar",
      },
      xaxis: {
        categories: Object.keys(metrics_dict), // Use keys from metrics_dict as categories
      },
    },
  };

  return (
    <div>
      <Card style={{ marginTop: "5%" }}>
        <h2>Thank you for taking the assessment!</h2>
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          {/* Bar Chart */}
          <div style={{ width: "45%" }}>
            <ReactApexChart
              options={barChartData.options}
              series={barChartData.series}
              type="bar"
              height={250}
            />
          </div>

          <div style={{ width: "45%" }}>
            <p>
              <b>Job Id :</b>
              {job_id}
            </p>
            <p>
              <b>Name :</b> {metrics.user_name}
            </p>
            <p>
              <b>Organisation :</b> {org}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
