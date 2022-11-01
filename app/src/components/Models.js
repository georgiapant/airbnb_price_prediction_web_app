import React from 'react'
import { useState } from "react";
import {
  Card,
  Typography,
  Form,
  Input,
  Select,
  Switch,
  Button,
  Divider,
} from "antd";
import { makeModelsPost } from "../api/api";
import {amenities} from "../data/amenities";
import {property_type} from "../data/property_type";
import { neighbourhood } from '../data/neighbourhoods';
import { host_ids } from '../data/host_ids';

const { Title } = Typography;
const { Option } = Select;

const formValuesInitialState = {
  host_id: "",
  latitude: "",
  longitude: "",
  maximum_nights: "",
  minimum_nights: "",
  accommodates: "",
  room_type: "",
  property_type:"",
  amenities: [],
  bathrooms:"",
  shared_bath: false,
  license: false,
  neighbourhood_cleansed:"",
  has_availability: false,
  instant_bookable: false,
  number_of_reviews:"",
  availability_90:""
  
};

const Models = () => {
  const [formValues, setFormValues] = useState(formValuesInitialState);
  const [models, setModels] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // console.log(name, value); // Uncomment to view name/value pair
    setFormValues({ ...formValues, [name]: value })
  };
  const handleSelectChange = (value) => {
    setFormValues({ ...formValues, room_type: value });
  };
  const handleSelectChangeWithSearch = (value) => {
    setFormValues({...formValues, property_type: value})
  };
  const handleSelectChangeWithSearch2 = (value) => {
    setFormValues({...formValues, neighbourhood_cleansed: value})
  };
  const handleMultipleSelectChange = (value) => {
    setFormValues({ ...formValues, amenities: value });
  };
  const handleSwitchChange1 = (value) => {
    setFormValues({ ...formValues, shared_bath: value});
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
    makeModelsPost(formValues).then((responseData) => {
      setModels(responseData);
    });


    // Make the POST HTTP request here
    // Sample POST file api/api.js
    //makeModelsPost(formValues).then((responseData) => {
    //  setModels(responseData);
    //});
  };

  const [btndisabled, setbtndisabled] = useState(true);
  const onValuesChange = (changedValues, allValues) => {

    if ( allValues.host_id !== undefined && allValues.latitude !== undefined && allValues.longitude !== undefined 
      && allValues.neighbourhood_cleansed !== undefined && allValues.maximum_nights !== undefined && allValues.minimum_nights !== undefined 
      && allValues.room_type !== undefined && allValues.property_type !== undefined 
      
      && allValues.host_id !== '' && allValues.latitude !== '' && allValues.longitude !== '' 
      && allValues.neighbourhood_cleansed !== '' && allValues.maximum_nights !== '' && allValues.minimum_nights !== '' 
      && allValues.room_type !== '' && allValues.property_type !== '' ) 
      {
      setbtndisabled(false);
    } else {
      setbtndisabled(true);
    }
    console.log(allValues);
  };


  return (
    <Card>
      {/* <div> 
        <FormErrors formErrors={validValues.formErrors.host_id} />
      </div> */}
      
      <Title>Models form</Title>
      <Form 
          onFinish={(values) => {
            console.log({ values });
          }}
          onFinishFailed={(error) => {
            console.log({ error });
          }}
          onValuesChange={onValuesChange}
        >
      {/* <form> */}
        <Form.Item label="Host ID" name="host_id" rules={[
              {
                required: true,
                message: "Please provide your host ID",
              },
              {
                validator: (_, value) =>
                  value && host_ids.includes(value)
                    ? Promise.resolve()
                    : Promise.reject("User ID is not valid"),
              },
            ]}
            hasFeedback
            >
          <Input
            placeholder=""
            name="host_id"
            value={formValues.host_id}
            onChange={handleInputChange}
            
          />
        </Form.Item>
        <Form.Item label="Latitude" name="latitude" rules={[
              {
                required: true,
                message: "Please enter a latitude",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
          <Input
            placeholder=""
            name="latitude"
            value={formValues.latitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Longitude" name="longitude" rules={[
              {
                required: true,
                message: "Please enter a longitude",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
          <Input
            placeholder=""
            name="longitude"
            value={formValues.longitude}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Neighbourhood" name="neighbourhood_cleansed" rules={[
              {
                required: true,
                message: "Please select a neighbourhood",
              },
            ]}
            hasFeedback>
          <Select

            name="neighbourhood_cleansed"
            showSearch
            optionFilterProp="children"
            value={formValues.neighbourhood_cleansed}
            onChange={handleSelectChangeWithSearch2}
            onSearch={handleSelectChangeWithSearch2}
            filterOption={(input, option) => option.children.toLowerCase().includes(input.toLowerCase())}

          >
           {neighbourhood.map((props)=> (
              <option key={props.id} value={props.val}>
                {props.val}
              </option>
            ))} 
          </Select>
        </Form.Item>


        <Form.Item label="Maximum nights of accommodation" name="maximum_nights" rules={[
              {
                required: true,
                message: "Please provide the maximum nights",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
          <Input
            placeholder=""
            name="maximum_nights"
            value={formValues.maximum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Minimun nights of accommodation" name="minimum_nights" rules={[
              {
                required: true,
                message: "Please provide the minimum nights",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
          <Input
            placeholder=""
            name="minimum_nights"
            value={formValues.minimum_nights}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Maximum number of guests" name="accommodates" rules={[
              {
                required: true,
                message: "Please provide the maximum number of guests",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
          <Input
            placeholder=""
            name="accommodates"
            value={formValues.accommodates}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Last 3 months availability" name="availability_90" rules={[
              {
                required: true,
                message: "Please provide the 3 months availability"
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}  
              hasFeedback>
          <Input
            placeholder=""
            name="availability_90"
            value={formValues.availability_90}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Number of reviews" name="number_of_reviews" rules={[
              {
                required: true,
                message: "Please provide number of reviews"
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
              hasFeedback>
          <Input
            placeholder=""
            name="number_of_reviews"
            value={formValues.number_of_reviews}
            onChange={handleInputChange}
            type='number'
          />
        </Form.Item>
        <Form.Item label="Room Type" name="room_type" rules={[
              {
                required: true,
                message: "Please select a room type",
              },
            ]}
            hasFeedback>
          <Select

            name="room_type"
            defaultValue=""
            value={formValues.room_type}
            onChange={handleSelectChange}
          >
            <Option value="">Please choose room type</Option>
            <Option value="Shared Room">Shared Room</Option>
            <Option value="Private Room">Private Room</Option>
            <Option value="Hotel Room">Hotel Room</Option>
            <Option value="Entire home/apt">Entire home or apartment</Option>
          </Select>
        </Form.Item>
        <Form.Item label="Property Type" name="property_type" rules={[
              {
                required: true,
                message: "Please select a property type",
              },
            ]}
            hasFeedback>
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
              <option key={prop.id} value={prop.val}>
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
              <option key={amenity.id} value={amenity.val}>
                {amenity.val}
              </option>
            ))}
           
          </Select>
        </Form.Item>
        <Form.Item label="Number of bathrooms" name="bathrooms" rules={[
              {
                required: true,
                message: "Please add number of bathrooms",
              },
              {
                validator: (_, value) =>
                  value && value>0
                    ? Promise.resolve()
                    : Promise.reject("Please enter a correct value"),
              },
            ]}
            hasFeedback>
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
            name="shared_bath"
            checked={formValues.shared_bath}
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
          <Button type="primary" onClick={handleFormSubmit} htmlType="submit" disabled={btndisabled}>
            Submit
          </Button>
        </Form.Item>
      </Form>

      <Divider />
      

      {models && (
        
        <div>
          <Title level={3}>{models['price']}</Title>       
        </div>
      )}
    </Card>
  );
};

export default Models;
