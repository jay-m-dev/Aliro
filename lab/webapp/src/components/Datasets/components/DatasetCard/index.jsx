/* ~This file is part of the Aliro library~

Copyright (C) 2023 Epistasis Lab, 
Center for Artificial Intelligence Research and Education (CAIRE),
Department of Computational Biomedicine (CBM),
Cedars-Sinai Medical Center.

Aliro is maintained by:
    - Hyunjun Choi (hyunjun.choi@cshs.org)
    - Miguel Hernandez (miguel.e.hernandez@cshs.org)
    - Nick Matsumoto (nicholas.matsumoto@cshs.org)
    - Jay Moran (jay.moran@cshs.org)
    - and many other generous open source contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

(Autogenerated header, do not modify)

*/
import React, { useState } from "react";
import { connect } from "react-redux";
import * as actions from "data/datasets/dataset/actions";
import DatasetActions from "./components/DatasetActions";
import BestResult from "./components/BestResult";
import ExperimentStatus from "./components/ExperimentStatus";
import {
  Grid,
  Segment,
  Header,
  Button,
  Popup,
  Message,
} from "semantic-ui-react";
import { formatDataset } from "../../../../utils/formatter";

const DatasetCard = ({ dataset, recommender, toggleAI }) => {
  const datasetLink = `/#/datasets/${dataset._id}`;
  const builderLink = `/#/builder?dataset=${dataset._id}`;

  var icon_type = "question circle";
  if (dataset.metafeatures._prediction_type == "classification") {
    icon_type = "list";
  } else if (dataset.metafeatures._prediction_type == "regression") {
    icon_type = "line graph";
  }

  // const [showGrid, setShowGrid] = useState(false);

  // const handleGridClick = () => {
  //   console.log("handleGridClick");
  //   setShowGrid(false);
  // };

  function clickDatasetCardDelButton(e) {
    let parent = e.target.closest(".dataset-card");
    // console.log(parent);
    // parent.style.cssText += ';display:none!important;';

    // find child which has <a> tag from the parent
    let child = parent.querySelector("a");

    // get the href attribute from the child
    let href = child.getAttribute("href");

    // parse the href to get the dataset id
    // and the last element is the dataset id
    let dataset_id = href.split("/").pop();

    // please show the popup to confirm the deletion of the dataset

    // Show the confirmation popup
    let confirmDelete = confirm(
      "Are you sure you want to delete the dataset with ID " + dataset_id + "?"
    );

    console.log("confirmDelete", confirmDelete);
    if (confirmDelete) {
      // User confirmed deletion, perform the deletion logic here
      console.log("confirmed deletion");
      removeDatasetCard(e);
    } else {
      // User canceled deletion, do nothing or perform any additional actions as needed
      // ...
      console.log("canceled deletion");
    }

    console.log("removed datasetcard", dataset_id);

    // api call to remove dataset
  }

  function removeDatasetCard(e) {
    let parent = e.target.closest(".dataset-card");
    console.log(parent);
    parent.style.cssText += ";display:none!important;";

    // find child which has <a> tag from the parent
    let child = parent.querySelector("a");

    // get the href attribute from the child
    let href = child.getAttribute("href");

    // parse the href to get the dataset id
    // and the last element is the dataset id
    let dataset_id = href.split("/").pop();

    console.log(dataset_id);

    // api call to remove dataset
  }

  function mouseEnterCardDelectButton(e) {
    console.log("mouseoverCardDelectButton");
    console.log(e.target);

    // make the red boundary in the trash can emoji
    e.target.style.cssText += ";border: 0.5px solid red;";
  }

  function mouseLeaveCardDelectButton(e) {
    console.log("mouseoverCardDelectButton");
    console.log(e.target);

    //REMOVE the red boundary in the trash can emoji
    e.target.style.cssText += ";border: 0px;";
  }

  if (
    document.getElementById("aiTooglePopup") == null &&
    document.getElementById("aiTooglePopupready") != null
  ) {
    // console.log("aiTooglePopup is null");
    // console.log(document.getElementById("aiTooglePopup"));

    // console.log("aiTooglePopupready is not null");
    // console.log(document.getElementById("aiTooglePopupready"));

    // remove div element widh id "aiTooglePopupready"
    var element = document.getElementById("aiTooglePopupready");
    element.parentNode.removeChild(element);

    function openTrueOrFalse_aiTooglePopup() {
      if (localStorage.getItem("aiTooglePopup") == "true") {
        return false;
      }
      // if localStorage does not have aiTooglePopup

      // document.getElementById("addNewPopup").style.cssText include "display: none;"
      else {
        return true;
      }
    }

    function openTrueOrFalse_buildNewExpPopup() {
      if (localStorage.getItem("buildNewExpPopup") == "true") {
        return false;
      }
      // if localStorage does not have buildNewExpPopup
      else {
        return true;
      }
    }

    return (
      // showGrid && (
      // <Grid.Column className="dataset-card" >
      <Grid.Column className="dataset-card">
        <Popup
          id="aiTooglePopup"
          trigger={
            <Segment inverted attached="top" className="panel-header">
              <Popup
                position="right center"
                header={formatDataset(dataset.name)}
                content={`Rows: ${dataset.metafeatures.n_rows}, Cols: ${dataset.metafeatures.n_columns}, Classes: ${dataset.metafeatures.n_classes}  Prediction type: ${dataset.files[0].prediction_type}`}
                trigger={
                  <Header
                    as="a"
                    inverted
                    size="large"
                    icon={icon_type}
                    content={formatDataset(dataset.name)}
                    href={datasetLink}
                    className="title"
                  />
                }
              />

              {/* cross x emoji */}
              {/* <span
                className="float-right"
                onClick={clickDatasetCardDelButton}
                onMouseEnter={mouseEnterCardDelectButton}
                onMouseLeave={mouseLeaveCardDelectButton}
                style={{ cursor: "pointer" }}
              >
                🗑
              </span> */}

              <span className="float-right">
                <DatasetActions
                  dataset={dataset}
                  recommender={recommender}
                  toggleAI={toggleAI}
                />
              </span>
            </Segment>
          }
          position="bottom right"
          // header={formatDataset(dataset.name)}
          content="Step 2: If you want to generate machine learning experiments automatically, please click to toggle AI button. Warning: when you toggle AI button, all tooltips will disappear."
          // make the open ture but display none

          open={openTrueOrFalse_aiTooglePopup()}
          // open = {false}
          // style={{display: "none !important"}}

          onClick={() => {
            if (document.getElementById("aiTooglePopup") != null) {
              document.getElementById("aiTooglePopup").style.cssText +=
                ";display:none !important;";

              // document.getElementById("buildNewExpPopup").style.cssText += ';display:block !important;';

              // save flag to local storage to avoid showing the popup again
              localStorage.setItem("aiTooglePopup", "true");
              // show the local storage on the console
              console.log(
                "aiTooglePopup",
                localStorage.getItem("aiTooglePopup")
              );

              // get class name content under id aiTooglePopup
              var content = document
                .getElementById("buildNewExpPopup")
                .getElementsByClassName("content")[0];
              // set border-radius: 10px;
              content.style.cssText += ";border-radius: 10px;";

              var buildNewExpPopup =
                document.getElementById("buildNewExpPopup");

              // set display: flex;
              buildNewExpPopup.style.cssText += ";display: flex;";
              // set flex-direction: row;
              buildNewExpPopup.style.cssText += ";flex-direction: row;";
              // set align-items: center;
              buildNewExpPopup.style.cssText += ";align-items: center;";

              // set animation: blinker 3s linear infinite;
              buildNewExpPopup.style.cssText +=
                ";animation: blinker 3s linear infinite;";
            }
          }}
        />

        <BestResult
          result={dataset.best_result}
          hasMetadata={dataset.has_metadata}
        />
        <ExperimentStatus
          filter={dataset._id}
          experiments={dataset.experiments}
          notifications={dataset.notifications}
        />
        <Popup
          id="buildNewExpPopup"
          trigger={
            <Button
              as="a"
              color="blue"
              attached="bottom"
              content="Build New Experiment"
              onClick={() => {
                localStorage.setItem("addNewPopup", "true");
                localStorage.setItem("aiTooglePopup", "true");
                localStorage.setItem("buildNewExpPopup", "true");
              }}
              href={builderLink}
            />
          }
          // content="Build a new experiment using this dataset"
          content="Step 3: Please click this button to build a machine learning experiment. 
        Warning: when you click this button, all tooltips will disappear."
          position="bottom center"
          // openOnTriggerClick
          // get information on whehter user click on the popup or not

          // first when web page is loaded, the popup should be shown
          // when user click on the popup, the popup should be hidden
          // on ={['click', 'hover']}

          open={openTrueOrFalse_buildNewExpPopup()}
          // open = {false}
          // style={{display: "none !important"}}

          onClick={() => {
            if (document.getElementById("buildNewExpPopup") != null) {
              document.getElementById("buildNewExpPopup").style.cssText +=
                ";display:none !important;";

              // addNewPopup

              // aiTooglePopup

              // buildNewExpPopup

              // save flag to local storage to avoid showing the popup again
              localStorage.setItem("buildNewExpPopup", "true");

              //  localStorage.setItem("aiTooglePopup", "true");

              //  localStorage.setItem("addNewPopup", "true");

              // show the local storage on the console
              console.log(
                "buildNewExpPopup",
                localStorage.getItem("buildNewExpPopup")
              );
            }
          }}
        />
      </Grid.Column>
    );
  } else {
    // console.log("aiTooglePopup is not null");
    // console.log(document.getElementById("aiTooglePopup"));

    // console.log("aiTooglePopupready is null");
    // console.log(document.getElementById("aiTooglePopupready"));

    return (
      <Grid.Column className="dataset-card">
        <Segment inverted attached="top" className="panel-header">
          <Popup
            position="right center"
            header={formatDataset(dataset.name)}
            content={`Rows: ${dataset.metafeatures.n_rows}, Cols: ${dataset.metafeatures.n_columns}, Classes: ${dataset.metafeatures.n_classes}  Prediction type: ${dataset.files[0].prediction_type}`}
            trigger={
              <Header
                as="a"
                inverted
                size="large"
                icon={icon_type}
                content={formatDataset(dataset.name)}
                href={datasetLink}
                className="title"
              />
            }
          />
          {/* cross x emoji */}
          {/* <span
            className="float-right"
            onClick={clickDatasetCardDelButton}
            onMouseEnter={mouseEnterCardDelectButton}
            onMouseLeave={mouseLeaveCardDelectButton}
            style={{ cursor: "pointer" }}
          >
            🗑
          </span> */}
          <span className="float-right">
            <DatasetActions
              dataset={dataset}
              recommender={recommender}
              toggleAI={toggleAI}
            />
          </span>
        </Segment>

        <BestResult
          result={dataset.best_result}
          hasMetadata={dataset.has_metadata}
        />
        <ExperimentStatus
          filter={dataset._id}
          experiments={dataset.experiments}
          notifications={dataset.notifications}
        />
        <Button
          as="a"
          color="blue"
          attached="bottom"
          content="Build New Experiment"
          href={builderLink}
        />
      </Grid.Column>
    );
  }

  // return (
  //   <Grid.Column className="dataset-card">

  //     <Segment inverted attached="top" className="panel-header">
  //       <Popup
  //         position="right center"
  //         header={formatDataset(dataset.name)}
  //         content={`Rows: ${dataset.metafeatures.n_rows}, Cols: ${dataset.metafeatures.n_columns}, Classes: ${dataset.metafeatures.n_classes}  Prediction type: ${dataset.files[0].prediction_type}`}
  //         trigger={
  //           <Header
  //             as="a"
  //             inverted
  //             size="large"
  //             icon={icon_type}
  //             content={formatDataset(dataset.name)}
  //             href={datasetLink}
  //             className="title"
  //           />
  //         }
  //       />
  //       <span className="float-right">
  //         <DatasetActions
  //           dataset={dataset}
  //           recommender={recommender}
  //           toggleAI={toggleAI}
  //         />
  //       </span>
  //     </Segment>

  //     <BestResult
  //       result={dataset.best_result}
  //       hasMetadata={dataset.has_metadata}
  //     />
  //     <ExperimentStatus
  //       filter={dataset._id}
  //       experiments={dataset.experiments}
  //       notifications={dataset.notifications}
  //     />
  //    <Button
  //         as="a"
  //         color="blue"
  //         attached="bottom"
  //         content="Build New Experiment"
  //         href={builderLink}
  //       />

  //   </Grid.Column>
  // );
};

export { DatasetCard };
export default connect(null, actions)(DatasetCard);

//  get aiTooglePopup id
//  if aiTooglePopup is not null, then hide it
// wait until document.getElementById("aiTooglePopup") loaded

setTimeout(function () {
  if (document.getElementById("aiTooglePopup") != null) {
    console.log("aiTooglePopup is not null");

    var aiTooglePopups = document.getElementById("aiTooglePopup");

    aiTooglePopups.style.cssText += ";display:none !important;";

    // length of aiTooglePopups
    var len = aiTooglePopups.length;
    console.log(len);

    // if (aiTooglePopups != null) {
    //   for (var i = 1; i < aiTooglePopups.length; i++) {
    //     aiTooglePopups[i].style.cssText += ';display:none !important;';
    //   }
    // }
  }
}, 100);
