import React, { useState } from "react";
import {
  MDBBtn,
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBRow,
  MDBCol,
  MDBIcon,
  MDBInput,
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";
import { login, register } from "../Services/Authentication"; // Import register function

function LoginPage() {
  const navigate = useNavigate();
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [organisation, setOrganisation] = useState("");
  const [organisationDesc, setOrganisationDesc] = useState("");
  const [role, setRole] = useState("");
  const [loginError, setLoginError] = useState(""); // State for login error message
  const [registrationError, setRegistrationError] = useState(""); // State for registration error message

  const handleLogin = async () => {
    try {
      const response = await login(username, password);
      if (response && response.Success) {
        sessionStorage.setItem("userData", JSON.stringify(response));
        navigate("/openings");
      } else {
        setLoginError("Invalid username or password");
      }
    } catch (error) {
      console.error("Login error:", error.message);
      setLoginError("Login failed. Please check your credentials.");
    }
  };

  const handleRegister = () => {
    setIsRegistering(true);
  };

  const handleSignIn = () => {
    setIsRegistering(false);
  };

  const handleRoleChange = (e) => {
    setRole(e.target.value);
  };

  const handleRegistrationSubmit = async () => {
    if (password !== confirmPassword) {
      setRegistrationError("Passwords do not match.");
      return;
    }

    try {
      const response = await register(
        role,
        username,
        password,
        organisation,
        organisationDesc
      );
      if (response && response.Success) {
        setIsRegistering(false);
        setRegistrationError("");
        setLoginError("Registration successful. Please login.");
      } else {
        setRegistrationError("Registration failed. Please try again.");
      }
    } catch (error) {
      console.error("Registration error:", error.message);
      setRegistrationError("Registration failed. Please try again.");
    }
  };

  return (
    <MDBContainer className="my-5">
      <MDBCard>
        <MDBRow className="g-0">
          <MDBCol md="6">
            <MDBCardImage
              src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/img1.webp"
              alt="login form"
              className="rounded-start w-100"
              style={{ height: "800px", objectFit: "cover" }}
            />
          </MDBCol>

          <MDBCol md="6">
            <MDBCardBody className="d-flex flex-column">
              <div className="d-flex flex-row mt-2">
                <MDBIcon
                  fas
                  icon="cubes fa-3x me-3"
                  style={{ color: "#ff6219" }}
                />
                <span className="h1 fw-bold mb-0">Welcome</span>
              </div>

              <h5
                className="fw-normal my-4 pb-3"
                style={{ letterSpacing: "1px" }}
              >
                {isRegistering
                  ? "Register an account"
                  : "Sign into your account"}
              </h5>

              {!isRegistering && (
                <>
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Email address"
                    id="formControlLg"
                    type="email"
                    size="lg"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Password"
                    id="formControlLg"
                    type="password"
                    size="lg"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />

                  <MDBBtn
                    className="mb-4 px-5"
                    color="dark"
                    size="lg"
                    onClick={handleLogin}
                  >
                    Login
                  </MDBBtn>
                  <a className="small text-muted" href="#!">
                    Forgot password?
                  </a>
                  <p className="mb-5 pb-lg-2" style={{ color: "#393f81" }}>
                    Don't have an account?{" "}
                    <button
                      className="btn btn-link p-0"
                      style={{ color: "#393f81" }}
                      onClick={handleRegister}
                    >
                      Register here
                    </button>
                  </p>

                  {/* Display login error message */}
                  {loginError && <p style={{ color: "red" }}>{loginError}</p>}
                </>
              )}

              {isRegistering && (
                <>
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Username"
                    id="username"
                    type="text"
                    size="lg"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Password"
                    id="password"
                    type="password"
                    size="lg"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Confirm Password"
                    id="confirmPassword"
                    type="password"
                    size="lg"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                  <select
                    className="form-select form-select-lg mb-4"
                    value={role}
                    onChange={handleRoleChange}
                  >
                    <option value="">Select Role</option>
                    <option value="candidate">Candidate</option>
                    <option value="recruiter">Recruiter</option>
                  </select>

                  {role !== "candidate" && (
                    <>
                      <MDBInput
                        wrapperClass="mb-4"
                        label="Add Organisation"
                        id="organisation"
                        type="text"
                        size="lg"
                        value={organisation}
                        onChange={(e) => setOrganisation(e.target.value)}
                      />
                      <MDBInput
                        wrapperClass="mb-4"
                        label="Add Organisation Description"
                        id="organisationDesc"
                        type="text"
                        size="lg"
                        value={organisationDesc}
                        onChange={(e) => setOrganisationDesc(e.target.value)}
                      />
                    </>
                  )}

                  <MDBBtn
                    className="mb-4 px-5"
                    color="dark"
                    size="lg"
                    onClick={handleRegistrationSubmit}
                  >
                    Submit
                  </MDBBtn>

                  <p className="mt-4 mb-0" style={{ color: "#393f81" }}>
                    Already have an account?{" "}
                    <button className="btn btn-link p-0" onClick={handleSignIn}>
                      Sign In here
                    </button>
                  </p>

                  {/* Display registration error message */}
                  {registrationError && (
                    <p style={{ color: "red" }}>{registrationError}</p>
                  )}
                </>
              )}

              <div className="d-flex flex-row justify-content-start">
                <a href="#!" className="small text-muted me-1">
                  Terms of use.
                </a>
                <a href="#!" className="small text-muted">
                  Privacy policy
                </a>
              </div>
            </MDBCardBody>
          </MDBCol>
        </MDBRow>
      </MDBCard>
    </MDBContainer>
  );
}

export default LoginPage;
