from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from osgeo import gdal
import time
import os

class AnalyzerInput(BaseModel):
    """Input schema for AnalyzerTool."""
    filepath: str = Field(..., description="Full filepath of the TIFF or JP2 file to be analyzed")

class AnalyzerTool(BaseTool):
    name: str = "analyze_file"
    description: str = (
        "Use this tool to analyze TIFF or JP2 raster files and extract their geographic bounding box coordinates. "
        "This tool will return the minx, miny, maxx, maxy values needed for geospatial processing. "
        "You MUST use this tool when asked to analyze any raster file."
    )
    args_schema: Type[BaseModel] = AnalyzerInput

    def _run(self, filepath: str) -> dict:
        # Implementation goes here
        start_time = time.time()
        print("analyze_tiff called")
        ds = gdal.Open(filepath)
        gt = ds.GetGeoTransform()
        minx = gt[0]
        maxy = gt[3]
        maxx = minx + (ds.RasterXSize * gt[1])
        miny = maxy + (ds.RasterYSize * gt[5])

        elapsed_time = time.time() - start_time

        return {
            "message": "JP2 analyzed successfully.",
            "minx": minx,
            "miny": miny,
            "maxx": maxx,
            "maxy": maxy,
            "filename": os.path.basename(filepath),
            "elapsed_time": elapsed_time
        }




class CropperInput(BaseModel):
        """Input schema for Crop Image Tool."""
        filepath: str = Field(..., description="Full filepath of the TIFF or JP2 file to be analyzed")
        crop_minx:     float = Field(..., description="Minx value of the bbox")
        crop_miny:     float = Field(..., description="Miny value of the bbox")
        crop_maxx:     float = Field(..., description="Maxx value of the bbox")
        crop_maxy:     float = Field(..., description="Maxy value of the bbox")

class CropperTool(BaseTool):
        name: str = "crop_image"
        description: str = (
            "Use this tool to crop TIFF or JP2 raster files and convert them to png. "
            "This tool will return the image_path value. "
            "You MUST use this tool when asked to crop any raster file."
        )
        args_schema: Type[BaseModel] = CropperInput

        def _run(self, filepath: str,crop_minx: float, crop_miny: float, crop_maxx: float, crop_maxy: float) -> dict:
            print("crop_image called")

            output_path = f'./{os.path.splitext(os.path.basename(filepath))[0]}_cropped.png'

            ds = gdal.Open(filepath)
            arr = ds.GetRasterBand(1).ReadAsArray()
            min_val = arr.min()
            max_val = arr.max()
            print(crop_minx, crop_miny, crop_maxx, crop_maxy)
            options = gdal.TranslateOptions(
                format='PNG',
                projWin=[crop_minx, crop_maxy, crop_maxx, crop_miny],
                outputType=gdal.GDT_Byte,
                scaleParams=[[float(min_val), float(max_val), 0, 255]]

            )

            gdal.Translate(output_path, filepath, options=options)
            return {"image_url": output_path}
