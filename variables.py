encabezado = '''<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>datosQuimicaGeo</se:Name>
    <UserStyle>
      <se:Name>datosQuimicaGeo</se:Name>
      <se:FeatureTypeStyle>
      '''
final = '''
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
'''
item = '''
        <se:Rule>
          <se:Name>%%index%%</se:Name>
          <se:Description>
            <se:Title>%%index%%</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>Estacion</ogc:PropertyName>
              <ogc:Literal>%%index%%</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:ExternalGraphic>
                <se:OnlineResource xlink:type="simple" xlink:href="%%path%%/Stiff-%%index%%.svg"/>
                <se:Format>image/svg+xml</se:Format>
              </se:ExternalGraphic>
              <se:Size>40</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
'''