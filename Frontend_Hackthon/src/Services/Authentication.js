import axios from "axios";
import { BASE_URL } from "../const";

export const login = async (username, password) => {
  const url = `${BASE_URL}/login?user=${encodeURIComponent(
    username
  )}&password=${encodeURIComponent(password)}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error.message);
    return null;
  }
};

export const register = async (
  userRoleId,
  username,
  password,
  orgName,
  orgDesc
) => {
  // Construct the URL with query parameters
  const url = `${BASE_URL}/signup?user_role_id=${encodeURIComponent(
    userRoleId
  )}&user=${encodeURIComponent(username)}&password=${encodeURIComponent(
    password
  )}&org_name=${encodeURIComponent(orgName)}&org_desc=${encodeURIComponent(
    orgDesc
  )}`;

  try {
    // Make a GET request to the registration endpoint
    const response = await axios.post(url);

    // Return the response data
    return response.data;
  } catch (error) {
    // Log the error message
    console.error("Registration failed:", error.message);

    // Return null if there is an error
    return null;
  }
};
