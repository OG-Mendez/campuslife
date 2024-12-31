import React, { useState } from "react";
import { Modal, Button, Dropdown, DropdownButton, Form } from "react-bootstrap";
import "rc-slider/assets/index.css";
import Slider from "rc-slider";
import "./FilterModal.css";

const FilterModal = ({ show, handleClose, applyFilters }) => {
  const [vacancy, setVacancy] = useState("Any");
  const [location, setLocation] = useState("Any");
  const [price, setPrice] = useState([60000, 600000]);

  const handleApplyFilters = () => {
    applyFilters({ vacancy, location, price });
    handleClose();
  };

  const handleInputChange = (index, value) => {
    const newPrice = [...price];
    newPrice[index] = Math.min(Math.max(value, 60000), 600000); // Clamp values between min and max
    if (newPrice[0] <= newPrice[1]) setPrice(newPrice); // Ensure min is less than or equal to max
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header className="c-btn" closeButton>
        <Modal.Title>
          <span className="ts-1">Search With Filter</span>
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Vacancy</Form.Label>
            <DropdownButton
              title={vacancy}
              onSelect={(selected) => setVacancy(selected)}
            >
              <Dropdown.Item eventKey="Any">Any</Dropdown.Item>
              <Dropdown.Item eventKey="Vacancy">Vacancy</Dropdown.Item>
              <Dropdown.Item eventKey="No vacancy">No vacancy</Dropdown.Item>
            </DropdownButton>
          </Form.Group>
          <hr />

          <Form.Group className="mb-3" >
            <Form.Label>Location</Form.Label>
            <DropdownButton
              title={location}
              onSelect={(selected) => setLocation(selected)}
              className="dropdown-btn"
            >
              <Dropdown.Item eventKey="Any">Any</Dropdown.Item>
              <Dropdown.Item eventKey="Eziobodo">Eziobodo</Dropdown.Item>
              <Dropdown.Item eventKey="Umuchima">Umuchima</Dropdown.Item>
            </DropdownButton>
          </Form.Group>
          <hr />

          <Form.Group>
  <Form.Label>Price : ₦</Form.Label>
  <div className="d-flex align-items-center">
    <Slider
      range
      min={60000}
      max={600000}
      value={price}
      onChange={(newPrice) => setPrice(newPrice)}
      className="w-100"
    />
  </div>
  <div className="price-input-container d-flex justify-content-between mt-2">
    <Form.Control
      type="text"
      value={price[0]}
      onChange={(e) => {
        const rawValue = e.target.value.replace(/[^\d]/g, ""); // Allow only numbers
        setPrice([Number(rawValue), price[1]]); // Update the min price only
      }}
      onBlur={(e) => {
        const rawValue = Number(e.target.value);
        handleInputChange(0, rawValue); // Apply clamping on blur
      }}
      className="price-input3"
    />
    <Form.Control
      type="text"
      value={price[1]}
      onChange={(e) => {
        const rawValue = e.target.value.replace(/[^\d]/g, ""); // Allow only numbers
        setPrice([price[0], Number(rawValue)]); // Update the max price only
      }}
      onBlur={(e) => {
        const rawValue = Number(e.target.value);
        handleInputChange(1, rawValue); // Apply clamping on blur
      }}
      className="price-input"
    />
  </div>
</Form.Group>


        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="warning"
          className="text-white"
          onClick={handleApplyFilters}
        >
          Apply Filter
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default FilterModal;