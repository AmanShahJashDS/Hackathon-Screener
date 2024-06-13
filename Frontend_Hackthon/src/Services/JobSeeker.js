import axios from "axios";
import { BASE_URL } from "../const";

export const fetchJobList = async (orgId) => {
  const url = `${BASE_URL}/job_list?org_id=${encodeURIComponent(orgId)}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch job list:", error.message);
    return null;
  }
};

export const uploadResume = async (job_id, pdfFile, org_id, user_name) => {
  const formData = new FormData();
  formData.append("pdf_file", pdfFile);
  const url = `${BASE_URL}/analysis?job_id=${encodeURIComponent(
    job_id
  )}&org_id=${encodeURIComponent(org_id)}&user_name=${encodeURIComponent(
    user_name
  )}`;

  try {
    const response = await axios.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Failed to fetch job list:", error.message);
    return null;
  }
};

export const submitButton = async (qa_pairs, user_id) => {
  const url = `${BASE_URL}/submit`;

  try {
    const response = await axios.post(url, qa_pairs, {
      params: {
        user_name: user_id,
      },
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Failed to submit data:", error.message);
    return null;
  }
};
