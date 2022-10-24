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
  amenities: [],
  radioField: "",
  shared_bathroom: false,
  license: false
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
  const handleMultipleSelectChange = (value) => {
    setFormValues({ ...formValues, amenities: value });
  };
  const handleSwitchChange1 = (value) => {
    setFormValues({ ...formValues, shared_bathroom: value});
  };
  const handleSwitchChange2 = (value) => {
    setFormValues({ ...formValues, license: value});
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
            placeholder="placeholder"
            name="hostID"
            value={formValues.hostID}
            onChange={handleInputChange}
          />
        </Form.Item>
        <Form.Item label="Latitude">
          <Input
            placeholder="placeholder"
            name="latitude"
            value={formValues.latitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Longitude">
          <Input
            placeholder="placeholder"
            name="longitude"
            value={formValues.longitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Maximum nights of accommodation">
          <Input
            placeholder="placeholder"
            name="maximum_nights"
            value={formValues.maximum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Minimun nights of accommodation">
          <Input
            placeholder="placeholder"
            name="minimum_nights"
            value={formValues.minimum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Maximum number of guests">
          <Input
            placeholder="placeholder"
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
       
        <Form.Item label="Amenities">
          <Select
            name="amenities"
            mode="multiple"
            allowClear
            value={formValues.amenities}
            onChange={handleMultipleSelectChange}
          >
            <Option value="select-1">Kitchen</Option>
            <Option value="select-2">Air conditioning</Option>
            <Option value="select-3">High end electronics</Option>
            <Option value="select-4">Barbeque</Option>
            <Option value="select-5">Balcony</Option>
            <Option value="select-6">Nature and views</Option>
            <Option value="select-7">Bed linen</Option>
            <Option value="select-8">Breakfast</Option>
            <Option value="select-9">TV</Option>
            <Option value="select-10">Coffee machine</Option>
            <Option value="select-11">Cooking basics</Option>
            <Option value="select-12">Elevator</Option>
            <Option value="select-13">Gym</Option>
            <Option value="select-14">Child friendly</Option>
            <Option value="select-15">Parking</Option>
            <Option value="select-16">Outdoor space</Option>
            <Option value="select-17">Host greeting</Option>
            <Option value="select-18">Hot tub sauna or pool</Option>
            <Option value="select-19">Internet</Option>
            <Option value="select-20">Long-term stays</Option>
            <Option value="select-21">Pets allowed</Option>
            <Option value="select-22">Private entrance</Option>
            <Option value="select-23">Secure</Option>
            
          </Select>
        </Form.Item>
        <Form.Item label="Radio groups">
          <Radio.Group
            name="radioField"
            onChange={handleInputChange}
            value={formValues.radioField}
          >
            <Radio value="radio-1">Radio 1</Radio>
            <Radio value="radio-2">Radio 2</Radio>
            <Radio value="radio-3">Radio 3</Radio>
            <Radio value="radio-4">Radio 4</Radio>
          </Radio.Group>
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
