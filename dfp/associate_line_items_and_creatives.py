import logging
from googleads import dfp

from dfp.client import get_client

logger = logging.getLogger(__name__)


def make_licas(line_item_ids, creative_ids, vast_line_item_ids, vast_creative_ids, size_overrides):
    """
    Attaches creatives to line items in DFP.

    Args:
      line_item_ids (arr): an array of line item IDs
      creative_ids (arr): an array of creative IDs
    Returns:
      None
    """
    dfp_client = get_client()
    lica_service = dfp_client.GetService(
        'LineItemCreativeAssociationService', version='v201802')

    sizes = []

    for size_override in size_overrides:
        sizes.append(size_override)

    vast_sizes = [
        {
            'width': '400',
            'height': '300'
        },
        {
            'width': '640',
            'height': '480'
        },
    ]

    licas = []
    vlicas = []
    for line_item_id in line_item_ids:
        for creative_id in creative_ids:
            licas.append({
                'creativeId': creative_id,
                'lineItemId': line_item_id,
                # "Overrides the value set for Creative.size, which allows the
                #  creative to be served to ad units that would otherwise not be
                #  compatible for its actual size."
                #    https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemCreativeAssociationService.LineItemCreativeAssociation
                #
                # This is equivalent to selecting "Size overrides" in the DFP
                # creative settings, as recommended:
                # http://prebid.org/adops/step-by-step.html
                'sizes': sizes
            })

    for vlid in vast_line_item_ids:
        for vast in vast_creative_ids:
            vlicas.append({
                'creativeId': vast,
                'lineItemId': vlid,
                'sizes': vast_sizes,
            })
    licas = lica_service.createLineItemCreativeAssociations(licas)

    vlicas = lica_service.createLineItemCreativeAssociations(vlicas)

    if licas:
        logger.info(
            u'Created {0} line item <> creative associations.'.format(
                len(licas)))
    else:
        logger.info(u'No line item <> creative associations created.')
