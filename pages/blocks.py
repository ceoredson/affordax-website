from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=60)
    url = blocks.CharBlock(max_length=240, help_text="A site path such as /employers/ or a full URL.")

    class Meta:
        icon = "link"


class FeatureBlock(blocks.StructBlock):
    number = blocks.CharBlock(max_length=12, required=False)
    title = blocks.CharBlock(max_length=90)
    text = blocks.TextBlock(max_length=280)


class FeatureGridBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=70, required=False)
    heading = blocks.CharBlock(max_length=120)
    intro = blocks.TextBlock(max_length=320, required=False)
    features = blocks.ListBlock(FeatureBlock(), min_num=2, max_num=6)

    class Meta:
        template = "pages/blocks/feature_grid.html"
        icon = "list-ul"
        label = "Feature grid"


class StepBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=90)
    text = blocks.TextBlock(max_length=280)


class ProcessBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=70, required=False)
    heading = blocks.CharBlock(max_length=120)
    steps = blocks.ListBlock(StepBlock(), min_num=2, max_num=6)

    class Meta:
        template = "pages/blocks/process.html"
        icon = "tasks"
        label = "Process"


class MetricBlock(blocks.StructBlock):
    value = blocks.CharBlock(max_length=32)
    label = blocks.CharBlock(max_length=120)


class MetricBandBlock(blocks.StructBlock):
    metrics = blocks.ListBlock(MetricBlock(), min_num=2, max_num=4)

    class Meta:
        template = "pages/blocks/metric_band.html"
        icon = "pick"
        label = "Metric band"


class EditorialBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=70, required=False)
    heading = blocks.CharBlock(max_length=140)
    body = blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])
    image = ImageChooserBlock(required=False)
    image_side = blocks.ChoiceBlock(choices=[("right", "Right"), ("left", "Left")], default="right")

    class Meta:
        template = "pages/blocks/editorial.html"
        icon = "doc-full"
        label = "Editorial story"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(max_length=360)
    attribution = blocks.CharBlock(max_length=120)
    role = blocks.CharBlock(max_length=120, required=False)

    class Meta:
        template = "pages/blocks/quote.html"
        icon = "openquote"
        label = "Quote"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=160)
    answer = blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])


class FAQBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=70, required=False)
    heading = blocks.CharBlock(max_length=120, default="Questions, answered")
    items = blocks.ListBlock(FAQItemBlock(), min_num=2, max_num=10)

    class Meta:
        template = "pages/blocks/faq.html"
        icon = "help"
        label = "Frequently asked questions"


class CallToActionBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=70, required=False)
    heading = blocks.CharBlock(max_length=130)
    text = blocks.TextBlock(max_length=320)
    primary = LinkBlock()
    secondary = LinkBlock(required=False)

    class Meta:
        template = "pages/blocks/call_to_action.html"
        icon = "plus-inverse"
        label = "Call to action"


PUBLIC_BLOCKS = [
    ("feature_grid", FeatureGridBlock()),
    ("process", ProcessBlock()),
    ("metric_band", MetricBandBlock()),
    ("editorial", EditorialBlock()),
    ("quote", QuoteBlock()),
    ("faq", FAQBlock()),
    ("call_to_action", CallToActionBlock()),
]

