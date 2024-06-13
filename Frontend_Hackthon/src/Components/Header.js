import React, { useState, useEffect } from "react";
import { Layout, Menu, Dropdown, Avatar, Input } from "antd";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { HomeOutlined, FileOutlined, ProfileOutlined, UserOutlined, LogoutOutlined, SearchOutlined } from "@ant-design/icons";

const { Header: AntHeader } = Layout;
const { Search } = Input;

export default function Header() {
  const location = useLocation();
  const navigate = useNavigate(); // Hook to navigate programmatically
  const [selectedKey, setSelectedKey] = useState("");

  useEffect(() => {
    switch (location.pathname) {
      case "/openings":
        setSelectedKey("1");
        break;
      case "/assessement":
        setSelectedKey("2");
        break;
      case "/screener":
        setSelectedKey("3");
        break;
      default:
        setSelectedKey("1"); // Default to Home
        break;
    }
  }, [location.pathname]);

  const handleMenuClick = (e) => {
    setSelectedKey(e.key);
  };

  const handleSignOut = () => {
    // Perform any sign-out logic here (e.g., clear tokens, etc.)
    navigate("/"); // Redirect to the home page
  };

  const handleSearch = (value) => {
    // Perform search logic here
    console.log("Searched for:", value);
  };

  const menu = (
    <Menu>
      <Menu.Item key="1" icon={<LogoutOutlined />} onClick={handleSignOut}>
        Sign Out
      </Menu.Item>
    </Menu>
  );

  return (
    <AntHeader
      style={{
        position: "fixed",
        zIndex: 1,
        width: "100%",
        display: "flex",
        alignItems: "center",
        backgroundColor: "#001529",
      }}
    >
      <div
        className="logo"
        style={{
          float: "left",
          color: "white",
          fontWeight: "bold",
          fontSize: "20px",
          marginRight: "20px",
        }}
      >
      Screener
      </div>
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[selectedKey]}
        onClick={handleMenuClick}
        style={{
          lineHeight: "64px",
          flex: 1,
          backgroundColor: "transparent",
          borderBottom: "none",
        }}
      >
        <Menu.Item
          key="1"
          icon={<HomeOutlined />}
          style={{
             color: selectedKey === "1" ? "white" : "#A8A8A8",
            padding: "0 20px"
           
           
          }}
        >
          <Link to="/openings">Home</Link>
        </Menu.Item>
       

      </Menu>
      <Search
        placeholder="Search Jobs"
        onSearch={handleSearch}
        style={{ width: 250, marginRight: "50px" }}
        enterButton={<SearchOutlined />}
      />
      <Dropdown overlay={menu} placement="bottomRight">
        <Avatar
          size="large"
          icon={<UserOutlined />}
          style={{ cursor: "pointer" }}
        />
      </Dropdown>
    </AntHeader>
  );
}
