import React from "react";
import { Layout, Row, Col, Typography } from "antd";
import { MailOutlined } from "@ant-design/icons";
import { FaInstagram, FaTwitter } from "react-icons/fa";

const { Footer: AntFooter } = Layout;
const { Text } = Typography;

function Footer() {
  return (
    <AntFooter
      style={{
        backgroundColor: "#001529",
        padding: "20px 50px",
        color: "#fff",
        textAlign: "center",
        flexShrink: 0,
        marginTop: "auto", // Ensures footer is pushed to the bottom
      }}
    >
      <Row
        justify="center"
        align="middle"
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Col span={24} style={{ marginBottom: "10px" }}>
          <Text style={{ color: "#A8A8A8" }}>Contact us: abc@abc.com</Text>
        </Col>
        <Col span={24}>
          <a
            href="mailto:abc@abc.com"
            style={{ color: "#fff", marginRight: "15px", fontSize: "20px" }}
            aria-label="Email"
          >
            <MailOutlined />
          </a>
          <a
            href="https://www.instagram.com/yourprofile"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#fff", marginRight: "15px", fontSize: "20px" }}
            aria-label="Instagram"
          >
            <FaInstagram />
          </a>
          <a
            href="https://www.twitter.com/yourprofile"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#fff", fontSize: "20px" }}
            aria-label="Twitter"
          >
            <FaTwitter />
          </a>
        </Col>
      </Row>
    </AntFooter>
  );
}

export default Footer;
