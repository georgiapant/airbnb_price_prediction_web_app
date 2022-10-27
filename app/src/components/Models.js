import React from 'react'
import { useState } from "react";
import {
  Card,
  Typography,
  Form,
  Input,
  Select,
  Radio,
  Switch,
  Button,
  Divider,
} from "antd";
import { makeModelsPost } from "../api/api";
import {amenities} from "../data/amenities";
import {property_type} from "../data/property_type";
import { neighbourhood } from '../data/neighbourhoods';

const { Title } = Typography;
const { Option } = Select;

const formValuesInitialState = {
  hostID: "",
  latitude: "",
  longitude: "",
  maximum_nights: "",
  minimum_nights: "",
  accommodates: "",
  room_type: "",
  property_type:"",
  amenities: [],
  radioField: "",
  bathrooms:"",
  shared_bathroom: false,
  license: false,
  neighbourhood:"",
  has_availability: false,
  instant_bookable: false
};

const Models = () => {
  const [formValues, setFormValues] = useState(formValuesInitialState);
  const [models, setModels] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // console.log(name, value); // Uncomment to view name/value pair
    setFormValues({ ...formValues, [name]: value });
  };
  const handleSelectChange = (value) => {
    setFormValues({ ...formValues, room_type: value });
  };
  const handleSelectChangeWithSearch = (value) => {
    setFormValues({...formValues, property_type: value})
  };
  const handleSelectChangeWithSearch2 = (value) => {
    setFormValues({...formValues, neighboorhoud: value})
  };
  const handleMultipleSelectChange = (value) => {
    setFormValues({ ...formValues, amenities: value });
  };
  const handleSwitchChange1 = (value) => {
    setFormValues({ ...formValues, shared_bathroom: value});
  };
  const handleSwitchChange2 = (value) => {
    setFormValues({ ...formValues, license: value});
  };
  const handleSwitchChange3 = (value) => {
    setFormValues({ ...formValues, has_availability: value});
  };
  const handleSwitchChange4 = (value) => {
    setFormValues({ ...formValues, instant_bookable: value});
  };
  const resetForm = () => {
    setFormValues(formValuesInitialState);
  };
  const handleFormSubmit = (e) => {
    e.preventDefault();
    console.log(formValues);

    // Make the POST HTTP request here
    // Sample POST file api/api.js
    makeModelsPost(formValues).then((responseData) => {
      setModels(responseData);
    });
  };

  return (
    <Card>
      <Title>Models form</Title>
      <form>
        <Form.Item label="Host ID">
          <Input
            placeholder=""
            name="hostID"
            value={formValues.hostID}
            onChange={handleInputChange}
          />
        </Form.Item>
        <Form.Item label="Latitude">
          <Input
            placeholder=""
            name="latitude"
            value={formValues.latitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Longitude">
          <Input
            placeholder=""
            name="longitude"
            value={formValues.longitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Neighbourhood">
          <Select

            name="neighbourhood"
            placeholder="Select a neighbourhood"
            showSearch
            optionFilterProp="children"
            value={formValues.property_type}
            onChange={handleSelectChangeWithSearch2}
            onSearch={handleSelectChangeWithSearch2}
            filterOption={(input, option) => option.children.toLowerCase().includes(input.toLowerCase())}

          >
           {neighbourhood.map((prop)=> (
              <option key={prop.id} value={prop.id}>
                {prop.val}
              </option>
            ))} 
          </Select>
        </Form.Item>


        <Form.Item label="Maximum nights of accommodation">
          <Input
            placeholder=""
            name="maximum_nights"
            value={formValues.maximum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Minimun nights of accommodation">
          <Input
            placeholder=""
            name="minimum_nights"
            value={formValues.minimum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Maximum number of guests">
          <Input
            placeholder=""
            name="accommodates"
            value={formValues.accommodates}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Room Type">
          <Select

            name="room_type"
            defaultValue=""
            value={formValues.room_type}
            onChange={handleSelectChange}
          >
            <Option value="">Please choose room type</Option>
            <Option value="select-1">Shared Room</Option>
            <Option value="select-2">Private Room</Option>
            <Option value="select-3">Hotel Room</Option>
            <Option value="select-4">Entire home or apartment</Option>
          </Select>
        </Form.Item>
        <Form.Item label="Property Type">
          <Select

            name="property_type"
            placeholder="Select a property type"
            showSearch
            optionFilterProp="children"
            value={formValues.property_type}
            onChange={handleSelectChangeWithSearch}
            onSearch={handleSelectChangeWithSearch}
            filterOption={(input, option) => option.children.toLowerCase().includes(input.toLowerCase())}

          >
           {property_type.map((prop)=> (
              <option key={prop.id} value={prop.id}>
                {prop.val}
              </option>
            ))} 
          </Select>
        </Form.Item>
        <Form.Item label="Amenities">
          <Select
            name="amenities"
            mode="multiple"
            allowClear
            value={formValues.amenities}
            onChange={handleMultipleSelectChange}
          >
            
            {amenities.map((amenity)=> (
              <option key={amenity.id} value={amenity.id}>
                {amenity.val}
              </option>
            ))}
           
          </Select>
        </Form.Item>
        <Form.Item label="Number of bathrooms">
          <Input
            placeholder=""
            name="bathrooms"
            value={formValues.bathrooms}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>

        <Form.Item label="Shared Bathroom">
          <Switch
            name="shared_bathroom"
            checked={formValues.shared_bathroom}
            onChange={handleSwitchChange1}
          />
        </Form.Item>
        <Form.Item label="Accommodation License">
          <Switch
            name="license"
            checked={formValues.license}
            onChange={handleSwitchChange2}
          />
        </Form.Item>

        <Form.Item label="Availability">
          <Switch
            name="has_availability"
            checked={formValues.has_availability}
            onChange={handleSwitchChange3}
          />
        </Form.Item>
        <Form.Item label="Instant Bookable">
          <Switch
            name="instant_bookable"
            checked={formValues.instant_bookable}
            onChange={handleSwitchChange4}
          />
        </Form.Item>

        <Form.Item>
          <Button type="secondary" onClick={resetForm}>
            Reset
          </Button>
          &nbsp;
          <Button type="primary" onClick={handleFormSubmit}>
            Submit
          </Button>
        </Form.Item>
      </form>

      <Divider />

      {models && (
        <div>
          <Title level={3}>Response data</Title>
          {JSON.stringify(models)}
        </div>
      )}
    </Card>
  );
};

export default Models;
