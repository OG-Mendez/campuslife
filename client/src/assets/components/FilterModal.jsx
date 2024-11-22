import React, { useState } from "react";
import { Modal, Button, Dropdown, DropdownButton, Form } from "react-bootstrap";
import "rc-slider/assets/index.css";
import Slider from "rc-slider";
import './FilterModal.css';

const FilterModal = ({ show, handleClose, applyFilters }) => {
  const [vacancy, setVacancy] = useState("Any");
  const [location, setLocation] = useState("Any");
  const [price, setPrice] = useState([60000, 260000]);

  // const resetFilters = () => {
  //   setVacancy("Any");
  //   setLocation("Any");
  //   setPrice([60000, 260000]);
  // };

  const handleApplyFilters = () => {
    applyFilters({ vacancy, location, price });
    // resetFilters();
    handleClose(); 
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header className="c-btn" closeButton>
        <Modal.Title><span className="ts-1">Search With Filter</span></Modal.Title>
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

          <Form.Group className="mb-3">
            <Form.Label>Location</Form.Label>
            <DropdownButton
              title={location}
              onSelect={(selected) => setLocation(selected)}
            >
              <Dropdown.Item eventKey="Any">Any</Dropdown.Item>
              <Dropdown.Item eventKey="Eziobodo">Eziobodo</Dropdown.Item>
              <Dropdown.Item eventKey="Umuchima">Umuchima</Dropdown.Item>
            </DropdownButton>
          </Form.Group>
          <hr />

          <Form.Group>
            <Form.Label>Price</Form.Label>
            <div className="d-flex align-items-center">
              <span>₦{price[0].toLocaleString()}</span>
              <Slider
                range
                min={60000}
                max={260000}
                value={price}
                onChange={(newPrice) => setPrice(newPrice)}
                className="mx-3"
              />
              <span>₦{price[1].toLocaleString()}</span>
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
